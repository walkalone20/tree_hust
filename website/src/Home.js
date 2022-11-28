/*
 * @Description:
 * @Author: LLNEyx
 * @Date: 2022-11-06 19:34:00
 * @LastEditors: LLNEyx
 */
import SideNav from "./components/SideNav";
import ItemListBar from "./components/ItemListBar";
import HomePageComposer from "./components/HomePageComposer";
import Intro from "./components/Intro";
import { useState,useEffect } from "react";
import Post from "./components/Post";

export default function Home(props) {
  
  useEffect(() => {
    setTimeout(() => {
      console.log('Aloha!')
      fetchPosts()
      console.log(1)
    }, 0); 
  }, [])
  

  function fetchPosts() {
    fetch("/post/", {
      method: "GET",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
      })
      .then((data) => {
        console.log("data")
        console.log(data)
        props.setPosts(data)
        console.log("posts")
        console.log(props.posts)
        console.log(props.postList)
      });
  }

  return (
    <div className="HomePageContent">
      <Intro mainTitle="HOME PAGE" subTitle="LOREM" length={props.postList.length}></Intro>
      <div className="container-fluid row">
        <div className="col-md-3 d-flex flex-column align-items-center">
          <br></br>
          <SideNav filterButtonList={props.filterButtonList}></SideNav>
        </div>
        <div className="col-md-9 ">
          {/* <button className="btn btn-outline-primary" onClick={fetchPosts}>111</button> */}
          <div class="list-group list-group-flush ItemList">
            <br></br>

            <div href="#" class="list-group-item rounded d-flex flex-column">
              {props.postList}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
