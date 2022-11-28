//回复帖子本身
export default function ReplyButton(props){
    const className="ReplyButton "+props.bsClass;

    return (
        <div className={className}>
            <button className="btn btn-success" type="button" data-bs-toggle="offcanvas" data-bs-target="#PostPageComposer" onClick={()=>props.onReply(0)}>
                回复本帖
            </button>
        </div>
    )
}