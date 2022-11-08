/*
 * @Description:
 * @Author: LLNEyx
 * @Date: 2022-11-06 15:04:41
 * @LastEditors: LLNEyx
 */
import PostButton from "./PostButton";


//todo 窗口窄的时候应该将这些都收到和topNavBar收起的link一起的地方
export default function SideNav(props) {
  return (
    <nav class="navbar">
      <div class="container-fluid d-flex flex-column">
        
        <PostButton ></PostButton>
        <br></br>

        <ul class="navbar-nav">
          {props.filterButtonList}
        </ul>
      </div>
    </nav>
  );
}
