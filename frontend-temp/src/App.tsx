import { useState } from "react";
import "./App.css";
import { Button, TextField } from "@mui/material";

export interface VanityEntry {
  inputNum: string;
  timestamp: number;
  vanityNums: string[];
}

function App() {
  // Was planning on setting up a quick and dirty way to directly query the database
  // Instead of setting up an API middleman to deal with that.
  const [databaseName, setDatabaseName] = useState<string>("");
  const [fetchedEntries, setFetchedEntries] = useState<VanityEntry[]>([
    {inputNum: "1-800-384-5729", timestamp: 0, vanityNums: ["+1 (800) WOW-OWOW", "+1 (800) WOW-OWOW", "+1 (800) WOW-OWOW"]},
    {inputNum: "1-800-384-5729", timestamp: 0, vanityNums: ["+1 (800) WOW-OWOW", "+1 (800) WOW-OWOW", "+1 (800) WOW-OWOW"]},
    {inputNum: "1-800-384-5729", timestamp: 0, vanityNums: ["+1 (800) WOW-OWOW", "+1 (800) WOW-OWOW", "+1 (800) WOW-OWOW"]},
  ]);

  const fetchEntries = (): void => {
    // Fetch
  };

  return (
    <div className="App">
      <div className="row">
        <TextField
          label="Database Name"
          value={databaseName}
          onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
            setDatabaseName(event.target.value);
          }}
        />
        <Button variant="contained" onClick={() => fetchEntries()}>
          Fetch
        </Button>
      </div>
      <div className="vanity-col">
        {/* Display the database entries in a row */}
        {fetchedEntries.map((entry, i) => (
          <div key={i} className="row vanity-row">
            <div>{entry.inputNum}</div>
            <div>
            {entry.vanityNums.map((vanity, j) => (
              <div key={j}>{vanity}</div>
            ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
