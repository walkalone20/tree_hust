import React from "react";
import LoginButton from "./LoginButton";
import SearchInput from "./SearchInput";
import "./BackTitle.css";
import { useState } from "react";
import DraftPost from "./DraftPost";

//todo 这里div里面的component都导入一下
export default function Header(props) {
  const [drafts, setDrafts] = useState([]);

  const draftList = drafts.map((d)=>{
    return <DraftPost tag={d.tag} title={d.draft_title} key={d.id} id={d.id} ></DraftPost>
  })

  function fetchDrafts() {
    fetch("/draft/", {
      method: "GET",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        'Authorization': "Token " + props.token,
      },
      redirect: "follow",
      referrerPolicy: "no-referrer",
    })
      .then((response) => {
        console.log('here is response')
        console.log(response);
        return response.json();
      })
      .then((data) => {
        console.log('lllll')
        console.log(data);
        setDrafts(data);
        console.log(draftList)
        props.uploadDrafts(draftList)
      });
  }

  return (
    <nav className="navbar navbar-expand-md navbar-dark bg-success fixed-top">
      
      <div className="container-fluid">
        <div className="navbar-brand">
          <button
            className="btn btn-sm rounded btn-success d-flex justify-content-between align-items-center"
            width="30px"
            onClick={props.onBack}
          >
            {/* <img
              src={require("../icons/back.png")}
              className="icon rounded-circle "
              width="30px"
              alt="Bootstrap"
            ></img> */}
            <span id="BackTitle">TreeHust</span>
          </button>
        </div>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#mynavbar"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="mynavbar">
          <ul className="navbar-nav ms-auto">
            {/* <form className="d-flex">
              <input className="form-control me-2" type="text" placeholder="Search"/>
              <button className="btn btn-primary" type="button">Search</button>
            </form> */}
            <SearchInput setPosts={props.setPosts}></SearchInput>

            <li className="nav-item draftLi ms-1">
              <button
                className="btn btn-seccess text-light "
                href="#DraftBox"
                role="button"
                data-bs-toggle="offcanvas"
                onClick={fetchDrafts}
              >
                draft
              </button>
            </li>

            {/* <li className="nav-item notificationLi">
              <a
                className="nav-link "
                href="#NotificationBox"
                role="button"
                data-bs-toggle="offcanvas"
              >
                notification
              </a>
            </li> */}

            <LoginButton
              token={props.token}
              onLogout={props.onLogout}
              isOnline={props.isOnline}
            ></LoginButton>
          </ul>
        </div>
      </div>
    </nav>
  );
}
