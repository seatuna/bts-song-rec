import useSWR from "swr";
import { useDebounce } from "./hooks/useDebounce";
import { fetcher } from "./utils";
import { ChangeEvent, Fragment, useState } from "react";

interface Song {
  spotify_id: string;
  name: string;
}

export const SongDropdown = () => {
  const [searchQuery, setSearchQuery] = useState<string>("");
  const debouncedSearchQuery = useDebounce(searchQuery) as string;
  const queryParams = new URLSearchParams({ query: debouncedSearchQuery });
  const { data, error, isLoading } = useSWR<Song[]>(
    queryParams && debouncedSearchQuery
      ? `http://localhost:5000/song/search?${queryParams}`
      : null,
    fetcher
  );

  const handleSearch = (event: ChangeEvent<HTMLInputElement>): void => {
    event.preventDefault();
    setSearchQuery(event.target.value);
  };

  const selectSong = (songId: string) => {
    console.log(songId);
  };

  console.log("debouncedSearchQuery:", debouncedSearchQuery);

  if (isLoading) {
    return <span>loading</span>;
  }

  if (error) {
    return <span>error</span>;
  }

  return (
    <>
      <form className="flex items-center">
        <label htmlFor="simple-search" className="sr-only">
          Search
        </label>
        <div className="relative w-full">
          <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
            <svg
              aria-hidden="true"
              className="w-5 h-5 text-indigo-900 dark:text-gray-400"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fillRule="evenodd"
                d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                clipRule="evenodd"
              ></path>
            </svg>
          </div>
          <input
            type="text"
            id="simple-search"
            className="bg-indigo-200 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-10 p-2.5  dark:bg-indigo-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-500 dark:focus:border-indigo-500"
            placeholder="Search"
            required
            onChange={handleSearch}
            value={searchQuery}
          />
        </div>
        <button
          type="submit"
          className="p-2.5 ml-2 text-sm font-medium text-white bg-indigo-700 rounded-lg border border-indigo-700 hover:bg-indigo-800 focus:ring-4 focus:outline-none focus:ring-indigo-300 dark:bg-indigo-600 dark:hover:bg-indigo-700 dark:focus:ring-indigo-800"
        >
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            ></path>
          </svg>
          <span className="sr-only">Search</span>
        </button>
      </form>

      {data && data.length > 0 ? (
        <>
          <h3 className="my-4 text-2xl font-extrabold leading-none tracking-tight text-gray-900 md:text-4xl dark:text-white">
            Search Results
          </h3>
          <Fragment>
            <ul className="space-y-1 text-gray-500 list-none list-inside dark:text-gray-400">
              {data.map((song: Song, i: number) => {
                return (
                  <li key={i} onClick={() => selectSong(song.spotify_id)}>
                    {song.name}
                  </li>
                );
              })}
            </ul>
          </Fragment>
        </>
      ) : (
        <h3 className="my-4 text-2xl font-extrabold leading-none tracking-tight text-gray-900 md:text-4xl dark:text-white">
          No Results
        </h3>
      )}
    </>
  );
};
