import { useState } from "react";

export default function LoginButton(props) {
  function logout() {
    fetch("/logout/", {
      method: "GET",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "Authorization":"Token "+props.token,
      },
      redirect: "follow",
      referrerPolicy: "no-referrer",
    }).then((response) => {
      if (response.ok) {
        alert("您已登出当前账户");
        props.onLogout();
      } else {
        alert(response.status + response.statusText);
      }
    });
  }

  const offlineButton = (
    <li className="nav-item dropdown profileLi">
      <button
        className="text-light btn btn-success ms-1"
        role="button"
        type="button"
        data-bs-toggle="modal"
        data-bs-target="#LoginModal"
      >
        Login
      </button>
    </li>
  );

  const onlineAnchor = (
    <li className="nav-item dropdown profileLi">
      <a
        className="nav-link dropdown-toggle "
        href="#"
        role="button"
        data-bs-toggle="dropdown"
      >
        <img
          src={require("../icons/person.png")}
          className="icon rounded-circle"
          width="20px"
          alt="profile"
        ></img>
      </a>
      <ul className="dropdown-menu dropdown-menu-end">
        <li>
          <button className="dropdown-item ">Link 111</button>
        </li>

        <li>
          <hr className="dropdown-divider"></hr>
        </li>

        <li>
          <button className="dropdown-item " onClick={logout}>
            Logout
          </button>
        </li>
      </ul>
    </li>
  );

  return props.isOnline ? onlineAnchor : offlineButton;
}
