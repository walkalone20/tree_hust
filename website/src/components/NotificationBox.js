import NotificationPost from "./NotificationPost";
import { useState } from "react";
export default function NotificationBox(props) {
  const [drafts, setDrafts] = useState();

  function deleteDraft(id) {
    const updatedDrafts = drafts.filter((draft) => draft.id !== id);
    setDrafts(updatedDrafts);
  }

  function editDraft() {}

  return (
    <div class="offcanvas offcanvas-end" id="NotificationBox">
      <div class="offcanvas-header">
        <h1 class="offcanvas-title">Notifications</h1>
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
        <NotificationPost></NotificationPost>
      </div>
    </div>
  );
}
