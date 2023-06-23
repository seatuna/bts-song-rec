import { useCallback, useEffect, useState } from "react";

export const useFetch = (url: string) => {
  const [data, setData] = useState();
  const [loading, setLoading] = useState(false);

  const getData = useCallback(async () => {
    setLoading(true);
    const response = await fetch(url);
    const result = await response.json();
    setData(result);
    setLoading(false);
  }, [url]);

  useEffect(() => {
    getData();
  }, [getData]);

  return { data, loading };
};