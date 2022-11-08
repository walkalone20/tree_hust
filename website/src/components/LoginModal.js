import { useState } from "react";

//todo LR切换的时候没有过渡动画
export default function LoginModal(props) {
  const [isLogin, setIsLogin] = useState(true);
  const [title1, setTitle1] = useState("Login");
  const [title2, setTitle2] = useState("Register");
  const [usr, setUsr] = useState("");
  const [email, setEmail] = useState("");
  const [pwd, setPwd] = useState("");
  const [pwd2, setPwd2] = useState("");

  function clearInputs() {
    setUsr("");
    setEmail("");
    setPwd("");
    setPwd2("");
    if (!isLogin) handleChangeLR();
  }

  function handleChangeUsr(e) {
    setUsr(e.target.value);
  }

  function handleChangeEmail(e) {
    setEmail(e.target.value);
  }

  function handleChangePwd(e) {
    setPwd(e.target.value);
  }

  function handleChangePwd2(e) {
    setPwd2(e.target.value);
  }

  function handleSubmit() {
    if (!isLogin) {
      fetch("/register/", {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, *cors, same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, *same-origin, omit
        headers: {
          "Content-Type": "application/json",
          // "Content-Type": "application/x-www-form-urlencoded",
        },
        redirect: "follow", // manual, *follow, error
        referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify({
          email: email,
          username: usr,
          password: pwd,
          password2: pwd2,
        }), // body data type must match "Content-Type" header
      })
        .then((response) => {
          console.log(response);
          return response.json();
        })
        .then((data) => {
          if (data.error) {
            alert(data.error);
          } else {
            alert("验证邮件已发送到您的邮箱，请前往确认。");
          }
        });
    } else {
      fetch("/login/", {
        method: "POST",
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
        },
        redirect: "follow",
        referrerPolicy: "no-referrer",
        body: JSON.stringify({
          username: email,
          password: pwd,
        }),
      })
        .then((response) => {
          console.log(response);
          return response.json();
        })
        .then((data) => {
          if (data.error) {
            alert(data.error);
          } else {
            props.onLoginSuccess(data);
            console.log('-----------------------'+data.token);
          }
        });
    }

    clearInputs();
  }

  function handleChangeLR() {
    var t = title1;
    setTitle1(title2);
    setTitle2(t);
    setIsLogin(!isLogin);
  }

  return (
    <div className="modal fade" id="LoginModal">
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">
          <div className="modal-header">
            <button
              className="border-0 btn h4 modal-title text-dark "
              onClick={handleChangeLR}
            >
              <p></p>
              <h4>
                {title1}
                <small> &gt; {title2}</small>
              </h4>
            </button>
            <button
              type="button"
              className="btn-close"
              data-bs-dismiss="modal"
              onClick={clearInputs}
            ></button>
          </div>

          <div className="modal-body">
            {!isLogin ? (
              <div className="form-floating mb-3 mt-3">
                <input
                  type="text"
                  className="form-control"
                  id="usrInput"
                  placeholder="Enter username"
                  name="usr"
                  value={usr}
                  onChange={handleChangeUsr}
                />
                <label htmlFor="usrInput">username</label>
              </div>
            ) : (
              <></>
            )}

            <div className="form-floating mb-3 mt-3">
              <input
                type="text"
                className="form-control"
                id="emailInput"
                placeholder="Enter email"
                name="email"
                value={email}
                onChange={handleChangeEmail}
              />
              <label htmlFor="emailInput">Email</label>
            </div>

            <div className="form-floating mt-3 mb-3">
              <input
                type="text"
                className="form-control"
                id="pwdInput"
                placeholder="Enter password"
                name="pswd"
                value={pwd}
                onChange={handleChangePwd}
              />
              <label htmlFor="pwdInput">Password</label>
            </div>

            {!isLogin ? (
              <div className="form-floating mb-3 mt-3">
                <input
                  type="text"
                  className="form-control"
                  id="pwdInput2"
                  placeholder="Repeat pwd"
                  name="pswd2"
                  value={pwd2}
                  onChange={handleChangePwd2}
                />
                <label htmlFor="pwdInput2">repeat password</label>
              </div>
            ) : (
              <></>
            )}
          </div>

          <div className="modal-footer d-flex justify-content-center">
            <button
              type="button"
              className="btn btn-outline-success"
              data-bs-dismiss="modal"
              onClick={handleSubmit}
            >
              submit
            </button>

            <button
              type="button"
              className="btn btn-outline-secondary"
              data-bs-dismiss="modal"
              onClick={clearInputs}
            >
              cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
