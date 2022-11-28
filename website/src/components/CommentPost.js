import { useState } from "react";

export default function CommentPost(props) {
  const [likes, setLikes] = useState(props.likes);

  function handleLike(id) {
    fetch("/post/" + id + "/upvote/", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + props.token,
      },
      credentials: "same-origin",
      body: JSON.stringify({ likes: 0 }),
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        setLikes(data.likes);
        console.log(likes);
      });
  }

  // function handleHate(id) {
  //   fetch('/post/'+id+'/downvote/',{
  //     method:'PUT',
  //     headers: {
  //       "Content-Type": "application/json",
  //       Authorization: "Token " + props.token,
  //     },
  //     credentials:"same-origin",
  //     body:JSON.stringify({hates:0})
  //   }).then((response)=>{
  //     return response.json()
  //   }).then((data)=>{
  //     console.log(data)
  //     setLikes(data.likes)
  //     console.log(likes)
  //   })
  // }

  function handleComment(p) {
    fetch("/post/comment/"+p.id+'/', {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + props.token,
      },
      credentials: "same-origin",
      body: JSON.stringify({
        comment_under:p.id,
        comment_content:p.content,
      }),
    }).then((response)=>{
      console.log(response)
      return response.json()
    }).then((data)=>{
      console.log(data)
    });
  }

  return (
    <div className="container column CommentPost mt-4">
      <div className="Comment container row CommentHeader d-flex flex-wrap">
        <div className="CommentAvatar col-md-1 rounded-circle d-flex justify-content-start align-items-center me-auto">
          {/* <img src={require("../icons/search.png")} className="img-fluid" alt="person thumbnail"></img> */}
          <img
            src={require("../" + props.avatar)}
            className="icon rounded-circle "
            width="40px"
            alt="Bootstrap"
          ></img>
        </div>
        <div className="CommentDescriptionInShort  col-md-11 d-flex flex-column align-items-start justify-content-end">
          <h5 className="CommentTitle">{props.name}</h5>
          <h6 className="DescriptionInShort"> {props.time}</h6>
        </div>
      </div>

      <div className="container">
        <div className="CommentBody col-md-11 ms-auto">{props.content}</div>
      </div>

      <div className="CommentFooter container d-flex justify-content-between align-items-end">
        <div className="BarLeft col-md-2">
          <div className="UpvoteNum ">
            <i className="bi bi-hand-thumbs-up"></i>
            <span>{likes}</span>
          </div>
        </div>
        <div className="BarRight col-md-4 ms-auto d-flex justify-content-end">
          <button
            className="CommentButton btn text-dark"
            onClick={() => handleComment({id:props.id,content:props.content})}
          >
            回复
          </button>
          <button
            className="UpvoteButton btn  text-dark"
            onClick={() => handleLike(props.id)}
          >
            <i className="bi bi-chevron-up"></i>
          </button>
          {/* <button
            className="DownvoteButton btn  text-dark"
            onClick={()=>handleHate(props.id)}
          >
            <i className="bi bi-chevron-down"></i>
          </button> */}
        </div>
      </div>
      <hr />
    </div>
  );
}
