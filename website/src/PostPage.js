import { useEffect, useState } from "react";
import CommentSideBar from "./components/CommentSideBar";
import Intro from "./components/Intro";
import CommentPost from "./components/CommentPost";

//todo 需要根据Post点击后 后台传过来的内容来确定Header内容
export default function PostPage(props) {
  const [comments, setComments] = useState([]);

  useEffect(() => {
    setTimeout(() => {
      console.log("Aloha!");
      fetchComments();
      console.log(1);
    }, 0);
  }, []);

  // function

  // id={cmt.id} tmp_name={cmt.tmp_name} avatar={cmt.avatar} cmt={cmt} comment_under={cmt.comment_under} reply_to={cmt.reply_to} likes={cmt.likes}  time={cmt.comment_time} content={cmt.comment_content}
  // <CommentPost name={comment.tmp_name} likes={comment.likes-comment.hates} time={comment.comment_time} content={comment.comment_content}></CommentPost>
  const commentList = comments.map((comment)=>(<CommentPost name={comment.tmp_name} likes={comment.likes-comment.hates} time={comment.comment_time} content={comment.comment_content} avatar={comment.avatar} id={comment.id} token={props.token}></CommentPost>))



  function addComment(comment) {
    setComments([...comments, comment]);
  }

  useEffect(() => {
    setTimeout(() => {
      console.log("go deeper!");
      console.log(props.post_id);
      fetchComments();
      console.log("!!");
    }, 0);
  }, []);

  function fetchComments() {
    fetch("/post/" + props.post_id + "/", {
      method: "GET",
    })
      .then((response) => {
        console.log("response");
        console.log(response);
        return response.json();
      })
      .then((data) => {
        console.log("data");
        console.log(data);
        setComments(data.post_comment);
        console.log("comments");
        console.log(comments);
        // console.log(commentList)
      });
  }

  function handleReply(pk) {
    fetch("/post/comment/" + pk + "/", {
      method: "POST",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + props.token,
      },
      redirect: "follow",
      referrerPolicy: "no-referrer",
      body: JSON.stringify({
        comment_under: props.post_id,
        comment_content: "sdfsdf",
      }),
    })
      .then((response) => {
        console.log(response);
        return response.json();
      })
      .then((data) => {
        console.log(data);
      });
  }

  function handleCollect(pk) {
    fetch('/post/'+pk+'/collect/', {
      method: "PUT",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + props.token,
      },
      redirect: "follow",
      referrerPolicy: "no-referrer",
      body: JSON.stringify({
        stars: 0,
      }),
    }).then((response) => {
      console.log(pk);
      console.log(response);
      return response.json()
    }).then((data)=>{
      console.log(data)
    });
  }

  return (
    <div className="PostPageContent">
      <Intro mainTitle={props.name} subTitle={props.tag} length={comments.length}></Intro>
      <div className="container-fluid d-flex flex-row-reverse flex-wrap">
        <div className="col-md-3 d-flex flex-column align-items-center">
          <br></br>
          <CommentSideBar
            onReply={handleReply}
            onCollect={handleCollect}
            post_id={props.post_id}
          ></CommentSideBar>
        </div>

        <div className="col-md-9 me-auto">{commentList}</div>
      </div>
    </div>
  );
}
