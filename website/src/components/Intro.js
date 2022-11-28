/*
 * @Description:
 * @Author: LLNEyx
 * @Date: 2022-11-05 01:20:03
 * @LastEditors: LLNEyx
 */
/*
 * @Description:
 * @Author: LLNEyx
 * @Date: 2022-11-05 01:20:03
 * @LastEditors: LLNEyx
 */
import React from "react";

export default function Intro(props) {
  return (
    <div className="IntroDiv bg-light d-flex flex-column">
      <br></br><br></br><br></br><br></br>
      <div className="h2 text-center">{props.mainTitle}</div>
      <div className="h4 text-center">{props.subTitle}{" 已加载post*"}{props.length}</div>
      <br></br>
    </div>
  );
}
