/*
 * @Description:
 * @Author: LLNEyx
 * @Date: 2022-11-03 20:35:13
 * @LastEditors: LLNEyx
 */
/*
 * @Description:
 * @Author: LLNEyx
 * @Date: 2022-11-03 20:35:13
 * @LastEditors: LLNEyx
 */
import React, { useState } from "react";

export default function Post(props) {
  function handleOpenPost(){
    props.onSkim({post_id:props.id,name:props.title})
  }

  return (
    <button className="btn btn-light mb-2" onClick={handleOpenPost}>
      <div className="Post container row">
        
        <div className="PostDescriptionInShort col-sm-10 d-flex flex-column align-items-start justify-content-end">
          <h5 className="PostTitle t-5">Title:{props.title}</h5>
          <h6 className="DescriptionInShort">
            <span>Tag:{props.tag} </span>发布于{props.time.substring(0,10)}{" "}{props.time.substring(11,19)}
          </h6>
        </div>
        <div className="PostAttr col-sm-2 d-flex flex-column align-items-end justify-content-center">
          <div className="AttrItems ">
            <div className="iconWithData">
              <i className="bi bi-chat-right"> </i>
              <span> {props.comments}</span>
            </div>
            <div className="iconWithData">
              <i class="bi bi-eye"> </i>
              <span> {props.watches}</span>
            </div>
          </div>
        </div>
      </div>
    </button>
  );
}
