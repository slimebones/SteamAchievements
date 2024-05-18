export abstract class CustomArrUtils
{
  public static tryFindIndexAndRemove<T>(
    arr: T[],
    predicate: (val: T) => boolean): boolean
  {
    const deldIndex = arr.findIndex(predicate);
    if (deldIndex === undefined)
    {
      return false;
    }
    arr.splice(deldIndex, 1);
    return true;
  }
}
