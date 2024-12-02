"""
Common utils used for Python Programming Language.
"""

import asyncio
import inspect
import json
import re
import sys
import time as native_time
import traceback
import types
from math import floor
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    Coroutine,
    NoReturn,
    Self,
    TypeAlias,
    TypeVar,
)

from typing_extensions import TypeIs

if TYPE_CHECKING:
    from io import TextIOWrapper

__all__ = [
    "Result",
    "StringCodedError",
    "is_error",
    "unwrap",
    "resultify_fn",
    "aresultify_fn",
    "to_coded_error",

    "Logger",
    "setup_var_dir",
    "get_var_dir",
    "get_var_log_dir",
]

CODE_ERR = "err"
CODE_NOT_FOUND_ERR = "not_found_err"
CODE_STATUS_ERR = "status_err"
CODE_PANIC = "panic"

def format_stack_summary(summary: traceback.StackSummary) -> str:
    return "".join(
        list(traceback.StackSummary.from_list(summary).format())).strip()

def get_as_str(err: Exception) -> str | None:
    s = None
    tb = err.__traceback__
    if tb:
        summary = traceback.extract_tb(tb)
        s = format_stack_summary(summary)
    return s

def set_traceback(
    err: Exception,
    skip_frames: int = 0,
    ignore_existing: bool = False,
):
    """
    Creates traceback for an err.

    If ``ignore_existing`` is true, and err already has a traceback, it will
    be overwritten. Otherwise for errs with traceback nothing will be done.

    Original err is not affected, modified err is returned. If nothing is done,
    the same err is returned without copying.

    Argument ``skip_frames`` defines how many frames to skip. This function
    or any nested function frames are automatically skipped.
    """
    if err.__traceback__ is not None and ignore_existing:
        err.__traceback__ = None

    # skip 2 frames - this call and this function call
    prev_tb: types.TracebackType | None = new_traceback(skip_frames + 2)

    err.__traceback__ = prev_tb

def new_traceback(skip_frames: int = 0) -> types.TracebackType | None:
    current_frame = inspect.currentframe()
    if current_frame is None:
        raise ValueError("unavailable to retrieve current frame")
    # always skip the current frame, additionally skip as many frames as
    # provided by skip_frames
    next_frame = current_frame
    while skip_frames > 0:
        if next_frame is None:
            raise ValueError(f"cannot skip {skip_frames} frames")
        next_frame = next_frame.f_back
        skip_frames -= 1

    prev_tb = None
    while next_frame is not None:
        tb = types.TracebackType(
            tb_next=None,
            tb_frame=next_frame,
            tb_lasti=next_frame.f_lasti,
            tb_lineno=next_frame.f_lineno)
        if prev_tb is not None:
            tb.tb_next = prev_tb
        prev_tb = tb
        next_frame = next_frame.f_back
    return prev_tb


class StringCodedError(Exception):
    def __init__(
        self,
        msg: str | None = None,
        code: str = CODE_ERR,
        *,
        skip_frames: int = 0,
    ) -> None:
        if not re.match(r"^[a-z][0-9a-z]*(_[0-9a-z]+)*$", code):
            panic(f"invalid code {code}")
        if skip_frames < 0:
            panic(f"`skip_frames` must be positive, got {skip_frames}")
        self.code = code
        self.msg = msg
        final = code
        if msg:
            final += ": " + msg
        # since we don't raise, for each err we create traceback dynamically
        # upon creation, and skip this function frame, as well as others,
        # if the caller's code need it
        set_traceback(self, 1 + skip_frames)
        super().__init__(final)

    def __hash__(self) -> int:
        return hash(self.code)

    def is_(self, code: str) -> bool:
        return self.code == code

    def is_any(self, *code: str) -> bool:
        return self.code in code

    @classmethod
    def from_exc(cls, exc: Exception) -> Self:
        return cls("; ".join(exc.args), skip_frames=1)

def panic(msg: str | None = None) -> NoReturn:
    raise StringCodedError(msg, CODE_PANIC)

T = TypeVar("T")
TException = TypeVar("TException", bound=Exception)

# In Python it would be better to use `tuple[T, Exc]`, but we want to
# conform with other languages, that are not Go, doesn't support tuples, but
# support unions.
#
# Moreover it would be difficult for Python to handle cases like
# tuple[T1, T2, T3, ..., Exc] with using a commonly defined types like
# this one.
#
# We don't use `T | Err` since we want to cover broader case with base class
# Exception. Instructions that require exception's code, may use fallback "err"
# if an exception is not an instance of coded Err.
Result: TypeAlias = T | Exception

def unwrap(r: Result[T]) -> T:
    if is_error(r):
        raise r
    return r

def resultify_fn(fn: Callable[[], T], *errs: type[Exception]) -> Result[T]:
    if not errs:
        errs = (Exception,)
    try:
        r = fn()
    except Exception as err:
        if not isinstance(err, errs):
            raise
        return err
    return r

async def aresultify_fn(
    fn: Coroutine[Any, Any, T], *errs: type[Exception]
) -> Result[T]:
    if not errs:
        errs = (Exception,)
    try:
        r = await fn
    except Exception as err:
        if not isinstance(err, errs):
            raise
        return err
    return r

def is_error(o: Result[T]) -> TypeIs[Exception]:
    """
    Name `ee` is chosen for shorter writing since this function will be used
    A LOT in our error handling strategy. It's like `err != nil`. Also, we
    don't want to interfere with common-used local-scope variables like `e`,
    `exc` or `err`.
    """
    return isinstance(o, Exception)

def to_coded_error(e: Exception | StringCodedError) -> StringCodedError:
    """
    Converts an exception to an error, but skips if it's already an Err.
    """
    if isinstance(e, StringCodedError):
        return e
    return StringCodedError.from_exc(e)

def get_object_qualname(obj: object):
    # ref: https://stackoverflow.com/a/2020083/14748231
    klass = obj.__class__
    module = klass.__module__
    if (
            module is None
            # avoid outputs like "builtins.str"
            or module == "builtins"):
        return klass.__qualname__
    return module + "." + klass.__qualname__

_var_dir: Path | None = None
_var_log_dir: Path | None = None

def setup_var_dir(dir: Path):
    """
    For the app deployment, we use concept of `var` dir, in which all the
    variable data is stored.

    In this utils module we provide a conventional interface to work with the
    var dir, as well as it's subdirectories, e.g. var/log.

    This function should be called at the setup of the application, as soon as
    possible, to ensure the var dir is correctly setup before doing anything
    else.
    """
    global _var_dir, _var_log_dir
    if _var_dir is not None and _var_dir != dir:
        # Do not allow to reset var dir.
        return
    _var_dir = dir
    _var_log_dir = Path(dir, "log")

def get_var_dir() -> Path:
    if _var_dir is None:
        panic("Unset var dir")
    return _var_dir

def get_var_log_dir() -> Path:
    if _var_log_dir is None:
        panic("Unset var dir")
    assert(_var_log_dir is not None)
    return _var_log_dir

class Logger:
    """
    Separates logs per domains. Designed to not raise exceptions, but return
    them via `Result`. Better to write to the void rather than panic because of
    writing lock.
    """

    _fullname_to_logger: dict[str, Self] = {}
    """
    Fullname: `<domain>.<name>`
    """

    def __init__(
        self, domain: str, name: str, stderr: bool = False
    ):
        self._domain = self._secure_name(domain)
        self._name = self._secure_name(name)
        self._fullname = self._domain + "." + self._name
        if self._fullname in self._fullname_to_logger:
            raise Exception(
                f"Logger with name `{name}` is already registered."
            )
        self._fullname_to_logger[self._fullname] = self

        self._dir = Path(get_var_log_dir(), self._domain)
        self._dir.mkdir(parents=True, exist_ok=True)
        self._path = Path(self._dir, f"{self._name}.log")
        self._file: TextIOWrapper | None = None
        self.stderr = stderr

    @classmethod
    def get_or_create(cls, domain: str, id: str) -> Self:
        """
        In case of creation: the logger will be immediatelly opened.
        """
        fullname = cls._secure_name(domain) + "." + cls._secure_name(id)
        if fullname in cls._fullname_to_logger:
            return cls._fullname_to_logger[fullname]
        l = cls(domain, id)
        l.open()
        return l

    def open(self) -> Result[None]:
        if self._file is not None:
            return None
        try:
            self._file = self._path.open("a+", encoding="utf-8")  # type: ignore
        except Exception as error:
            return error

    def log_flex(self, v: Any, *, not_err_prefix: str = "") -> Result[None]:
        """
        Choose appropriate logging procedure based on incoming value.
        """
        if is_error(v):
            return self.error(v)
        return self.write(not_err_prefix + str(v))

    @staticmethod
    def _secure_name(name: str) -> str:
        return re.sub(r"[^a-z0-9_-]", "_", name)

    def _get_error_message(self, e: Exception) -> str:
        m = ""
        if isinstance(e, StringCodedError):
            m =  ",".join(e.args) + f"(Code {e.code})"
        else:
            m = ",".join(e.args)
        return m

    def commented_error(self, e: Exception, comment: str) -> Result[None]:
        """
        Same as error(), but prefix with `comment`.
        """
        m = self._get_error_message(e)
        if comment.endswith("."):
            comment = comment[:-1]
        m = comment + ": " + m
        return self.write(m, track=e)

    def error(self, e: Exception) -> Result[None]:
        m = self._get_error_message(e)
        return self.write(m, track=e)

    def write(
        self,
        *msg: str,
        sep: str = " ",
        end: str = "\n",
        track: Exception | None = None
    ) -> Result[None]:
        if self._file is None:
            return StringCodedError("No opened file")
        final_message = sep.join(msg) + end
        if track:
            final_message = self._track(final_message, track)

        data = {
            "time": time(),
            "message": final_message
        }
        if self.stderr:
            # Put additional newline for better stderr readability.
            print(final_message, end="\n", file=sys.stderr)  # noqa: T201
        self._file.write(json.dumps(data) + "\n")
        self._file.flush()

    def close(self):
        """
        Closes the logger file and removes the logger from the cache.
        """
        if self._file is None or self._file.closed:
            return
        self._file.close()
        self._file = None
        self._fullname_to_logger.pop(self._name, None)

    @staticmethod
    def _try_get_err_traceback_str(e: Exception) -> str | None:
        """
        Copy of err_utils.try_get_traceback_str to avoid circulars.
        """
        s = None
        tb = e.__traceback__
        if tb:
            extracted_list = traceback.extract_tb(tb)
            s = ""
            for item in traceback.StackSummary.from_list(
                    extracted_list).format():
                s += item
        return s

    @staticmethod
    def _get_err_msg(e: Exception) -> str:
        return ", ".join([str(a) for a in e.args])

    def _track(self, msg: str, e: Exception) -> str:
        final_msg = self._try_get_err_traceback_str(e)

        if not final_msg:
            final_msg = ""
        # for filled content, append newline operator to separate
        # traceback from err dscr
        elif not final_msg.endswith("\n"):
            final_msg += "\n"

        # add err dscr
        e_msg = self._get_err_msg(e)
        e_dscr = get_object_qualname(e)
        if e_msg:
            e_dscr += ": " + e_msg
        final_msg += e_dscr + "\n\n"
        final_msg += f"Extra message: {msg}"
        return final_msg

time_data = native_time.struct_time
Time = int
"""
Default time is int64, expressed in milliseconds.

If other is not specified, the time is always int64, milliseconds. Otherwise,
it must have a postfix `_<precision>sec`, e.g. `created_sec`. We've decided
that seconds are too broad (especially for a game engine), nano seconds are
too precise (in most cases), but milliseconds is a good middle ground.

Even in the long future, the default milliseconds should remain the same, even
if the digital interaction become super fast so it the time format would need
more precision.

Also, we're not big fans for transferring data in strings of any ISO format.
It makes parsing and comparing harder, while plain integers looks more
flexible.
"""
FloatSecTime = float
"""
Time measured in seconds with fractional part. We used to operate with that,
but now, by default, we use milliseconds, and an integer type.
"""

def time():
    return floor(native_time.time() * 1000)

def time_sleep(t: Time):
    """
    Sleep for amount of milliseconds.
    """
    native_time.sleep(t / 1000)

async def time_asleep(t: Time):
    await asyncio.sleep(t / 1000)

def time_local() -> time_data:
    return native_time.localtime()

def time_delta(delta: int, from_: int | None = None) -> int:
    """
    Calculates delta timestamp from "from_" (current moment by default) adding
    given delta.
    """
    from_ = from_ if from_ is not None else time()
    return from_ + delta

def time_format(f: str, data: time_data | None = None):
    return native_time.strftime(f, data if data is not None else time.gmtime())

def secure(fn: Callable[[], Result[T]]) -> Result[T]:
    try:
        return fn()
    except Exception as error:
        return error

async def asecure(fn: Callable[[], Awaitable[Result[T]]]) -> Result[T]:
    try:
        return await fn()
    except Exception as error:
        return error

def resultify(fn: Callable[[], T]) -> Result[T]:
    try:
        return fn()
    except Exception as error:
        return error

async def aresultify(fn: Callable[[], Awaitable[T]]) -> Result[T]:
    try:
        return await fn()
    except Exception as error:
        return error
