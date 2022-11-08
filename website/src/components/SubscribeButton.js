/*
 * @Description: 
 * @Author: LLNEyx
 * @Date: 2022-11-07 00:46:53
 * @LastEditors: LLNEyx
 */
//关注帖子以得到最新通知
//todo 对应的取关按钮需要颜色
export default function SubscribeButton(props){
    const className="SubscribeButton "+props.bsClass;

    return (
        <div className={className}>
            <button className="btn btn-outline-secondary" type="button" onClick={()=>props.onCollect(props.post_id)}>
                关注本帖
            </button>
        </div>
    )
}