import { useState,useEffect } from "react";
import DraftPost from "./DraftPost";
import "./DropDraft.css"
export default function DraftBox(props) {

  return (
    <div class="offcanvas offcanvas-end z-index-2" id="DraftBox">
      <div class="offcanvas-header">
        <h1 class="offcanvas-title">Draft-Box</h1>
        <div className="d-flex justify-content-end align-items-center">
          <button type="button" className="btn text-reset">
            <i class="bi bi-trash" id="DropDraft"></i>
          </button>
          <button
            type="button"
            class="btn-close text-reset"
            data-bs-dismiss="offcanvas"
          ></button>
        </div>
      </div>
      <hr className="w-100"></hr>
      <div class="offcanvas-body">
        {props.draftList}
      </div>
    </div>
  );
}
