/*
 * @Description:
 * @Author: LLNEyx
 * @Date: 2022-11-05 02:01:17
 * @LastEditors: LLNEyx
 */
import React, { useState } from "react";
// import "./SearchInput.css"

export default function SearchInput(props) {
  const className = "input-group SearchInput " + props.colPara;
  const [searchKey, setSearchKey] = useState("");

  function handleChange(e) {
    setSearchKey(e.target.value);
  }

  function handleSubmit(e) {
    fetch("/post/?search="+searchKey, {
      method: "GET",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
      })
      .then((data) => {
        console.log("data")
        console.log(data)
        console.log(searchKey)
        props.setPosts(data)
      });
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className={className}>
        <input
          placeholder="type something"
          type="text"
          autoComplete="off"
          value={searchKey}
          onChange={handleChange}
          className="inputSearch form-control border-0"
        />
        <button
          className="btn btn-outline-light"
          type="submit"
          onSubmit={handleSubmit}
        >
          {/* <img src={require("../icons/search.png")} className="searchIcon" alt="search-icon"/> */}
          Search
        </button>
      </div>
    </form>
  );
}
