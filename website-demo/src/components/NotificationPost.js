export default function NotificationPost(props) {
  return (
    <button className="btn rounded NotificationPost d-flex justify-content-between w-100 align-items-center">
      <div className="NotificationPostAvatar col-sm-2">
        <img
          src={require("../icons/person.png")}
          className="icon rounded-circle "
          width="40px"
          alt="Bootstrap"
        ></img>
      </div>

      <div className="NotificationPostDescriptionInShort col-sm-8 d-flex flex-column align-items-start justify-content-end">
        <h5 className="NotificationPostTitle t-5">
          title
          <small>{" tag"}</small>
        </h5>
        <h6 className="ContentInShort">lorem......</h6>
      </div>

      <div className="NotificationPostAttr col-sm-2 d-flex flex-column align-items-end justify-content-center">
        <div className="AttrItems ">
          <button className="btn mb-1">
            <i className="bi bi-trash"></i>
          </button>
        </div>
      </div>
    </button>
  );
}
