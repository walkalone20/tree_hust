/*
 * @Description:
 * @Author: LLNEyx
 * @Date: 2022-11-06 16:07:30
 * @LastEditors: LLNEyx
 */
import { useState } from "react";
export default function PostPageComposer(props) {
  const [hpcc, setHpcc] = useState(""); //home page composer content(正文)
  const [hpct, setHpct] = useState(""); //title
  const [hpcs, setHpcs] = useState(1); //section with default value 1

  var markdown = require("markdown").markdown;
  const [toHtml, setToHtml] = useState(markdown.toHTML(""));

  function handleChangeHpcc(e) {
    setHpcc(e.target.value);
    setToHtml(markdown.toHTML(hpcc));
  }

  function handleChangeHpct(e) {
    setHpct(e.target.value);
  }

  function handleChangeHpcs(e) {
    setHpcs(e.target.value);
  }

  function handleSubmit() {
    fetch("/post/create/", {
      method: "POST",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Token " + props.token,
      },
      redirect: "follow",
      referrerPolicy: "no-referrer",
      body: JSON.stringify({
        post_title: hpct,
        post_content: toHtml,
        tag: hpcs,
      }),
    })
      .then((response) => {
        console.log(props.token);
        console.log(hpcc, hpct, hpcs);
        console.log(response);
        if (response.ok) {
          return response.json();
        }
      })
      .then((data) => {
        console.log("?" + data);
      });
  }

  function saveAsDraft() {
    fetch("/draft/create/", {
      method: "POST",
      mode: "cors",
      cache: "no-cache",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Token " + props.token,
      },
      redirect: "follow",
      referrerPolicy: "no-referrer",
      body: JSON.stringify({
        draft_title: hpct,
        draft_content: hpcc,
        tag: hpcs,
      }),
    }).then((response) => {
      console.log(response);
    });
  }

  return (
    <div className="offcanvas offcanvas-bottom h-50" id="PostPageComposer">
      <div className="PostComposerTitle mt-3 d-flex align-items-center justify-content-between ">
        <div className="SectionAndTitle d-flex justify-content-start">
          <div className="BarLeft">
            <select
              className="form-select border-0 rounded-start"
              value={hpcs}
              onChange={handleChangeHpcs}
            >
              <option>1</option>
              <option>2</option>
              <option>3</option>
              <option>4</option>
            </select>
          </div>
          <input
            type="text"
            className="border-0 rounded ms-2 lead "
            placeholder="COMMENT TITLE"
            id="PostComposerTitleInput"
            value={hpct}
            onChange={handleChangeHpct}
          />
        </div>
        <div className="d-flex justify-content-end align-items-center">
          <button
            type="button"
            className="btn"
            data-bs-dismiss="offcanvas"
            onClick={saveAsDraft}
          >
            <i class="bi bi-save"></i>
          </button>
          <button
            type="button"
            className="btn-close"
            data-bs-dismiss="offcanvas"
          ></button>
        </div>
      </div>
      <hr className="vw-100"></hr>
      <div className="offcanvas-body">
        <textarea
          class="form-control"
          rows="5"
          id="comment"
          name="text"
          value={hpcc}
          placeholder="MARKDOWN"
          onChange={handleChangeHpcc}
        ></textarea>
        <button
          className="btn btn-outline-primary mt-2"
          type="button"
          onClick={handleSubmit}
        >
          submit
        </button>
      </div>
    </div>
  );
}
