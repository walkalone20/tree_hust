import ReplyButton from "./ReplyButton";
import SubscribeButton from "./SubscribeButton";
import "./CommentSideBar.css"
export default function CommentSideBar(props) {
  return (
    <nav className="navbar" id="CommentSideBar" >
      <div className="container-fluid d-flex flex-column " >
        <ReplyButton onReply={props.onReply}></ReplyButton>
        <br></br>
        <SubscribeButton onCollect={props.onCollect} post_id={props.post_id}></SubscribeButton>
      </div>
    </nav>
  );
}
