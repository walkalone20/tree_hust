/*
 * @Description: 
 * @Author: LLNEyx
 * @Date: 2022-11-05 01:21:07
 * @LastEditors: LLNEyx
 */
/*
 * @Description: 
 * @Author: LLNEyx
 * @Date: 2022-11-05 01:21:07
 * @LastEditors: LLNEyx
 */
export default function PostButton(props){
    const className="PostButton "+props.bsClass;

    return (
        <div className={className}>
            <button className="btn btn-success" type="button" data-bs-toggle="offcanvas" data-bs-target="#HomePageComposer">
                发布话题
            </button>
        </div>
    )
}