/*
 * @Description:
 * @Author: LLNEyx
 * @Date: 2022-10-31 20:35:19
 * @LastEditors: LLNEyx
 */
// import './App.css';
import Header from "./components/Header";
import Home from "./Home";
import PostPage from "./PostPage";
import { useState } from "react";
import HomePageComposer from "./components/HomePageComposer";
import PostPageComposer from "./components/PostPageComposer";
import LoginModal from "./components/LoginModal";
import DraftBox from "./components/DraftBox";
import NotificationBox from "./components/NotificationBox";
import Post from "./components/Post";

const FILTER_MAP = {
  tag0: () => true,
  tag1: (a) => a.tag === "1",
  tag2: (a) => a.tag === "2",
  tag3: (a) => a.tag === "3",
};

const FILTER_NAMES = Object.keys(FILTER_MAP);

function App() {
  const [inPost, setInPost] = useState(false);
  const [nowToken, setNowToken] = useState("");
  const [nowUserId, setNowUserId] = useState("");
  const [nowUserName, setNowUserName] = useState("");
  const [nowEmail, setNowEmail] = useState("");
  const [isOnline, setIsOnline] = useState(false);
  const [targetPost, setTargetPost] = useState(0);
  const [postName,setPostName] = useState('TITLE')


  const [posts, setPosts] = useState([]);
  const [filter, setFilter] = useState("tag0");
  const filterButtonList = FILTER_NAMES.map((name) => (
    <li class="nav-item">
      <button class="btn btn-outline-lignt " onClick={()=>setFilter(name)}>
        {name}
      </button>
    </li>
  ));
  const postList = posts.filter(FILTER_MAP[filter]).map((post) => {
    // console.log(post);
    const postObj = (
      <Post
        id={post.id}
        key={post.id}
        title={post.post_title}
        time={post.last_modified}
        comments={post.comments}
        tag={post.tag}
        watches={post.watches}
        onSkim={routeToPost}
      ></Post>
    );
    // console.log(postObj);
    return postObj;
  });

  function handleAddPost(post) {
    setPosts([...posts, post]);
  }

  const [drafts,setDrafts] = useState()
  
  function deleteDraft(id){
    const updatedDrafts = drafts.filter((draft)=>draft.id!==id)
    setDrafts(updatedDrafts)
  }

  function editDraft(){
    
  }

  const mainContent = inPost ? (
    <PostPage post_id={targetPost} name={postName} token={nowToken}></PostPage>
  ) : (
    <Home
      postList={postList}
      setPosts={setPosts}
      token={nowToken}
      filterButtonList={filterButtonList}
    ></Home>
  );

  function handleSearch(newPosts) {}

  function handleLogin(response) {
    console.log("token:" + response.token);
    setNowToken(response.token);
    setNowUserId(response.user_id);
    setNowUserName(response.username);
    setNowEmail(response.email);
    setIsOnline(true);
    // console.log([nowToken,nowUserId,nowUserName,nowEmail])
  }

  function handleLogout() {
    setNowToken("");
    setNowUserId("");
    setNowUserName("");
    setNowEmail("");
    setIsOnline(false);
  }

  function routeToPost(p) {
    setTargetPost(p.post_id);
    setPostName(p.name)
    setInPost(true);
  }

  function routeToHome() {
    setInPost(false);
  }

  const [dl,setDl] = useState([])
  // const [dlf,setDlf] = useState(null)
  function handleDrafts(d){
    setDl(d)
    // setDlf(d.deleteDraft)
  }

  return (
    <div className="App">
      <Header
        onBack={routeToHome}
        isOnline={isOnline}
        onLogout={handleLogout}
        token={nowToken}
        setPosts={setPosts}
        uploadDrafts={handleDrafts}
      ></Header>
      <DraftBox draftList={dl} ></DraftBox>
      <NotificationBox></NotificationBox>
      <LoginModal onLoginSuccess={handleLogin}></LoginModal>
      {mainContent}
      <HomePageComposer token={nowToken} onAddPost={handleAddPost} haha="asdf"></HomePageComposer>
      <PostPageComposer></PostPageComposer>
    </div>
  );
}

export default App;
