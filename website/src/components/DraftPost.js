export default function DraftPost(props) {
  
  function deleteDraft(){
    fetch("/draft/"+props.id+"/delete/", {
      method: "DELETE",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        'Authorization': "Token " + props.token,
      },
      redirect: "follow",
      referrerPolicy: "no-referrer",
      body:{tag:props.id}
    })
      .then((response) => {
        console.log('here is response!!!')
        console.log(response);
        return response.json();
      })
      .then((data) => {
        
      });
  }
  
  return (
    <button className="btn rounded DraftPost d-flex justify-content-between w-100 align-items-center">
      <div className="DraftPostDescriptionInShort col-sm-10 d-flex flex-column align-items-start justify-content-end">
        <h5 className="DraftPostTitle t-5">
          {props.title}
          <small>
            {' tag'+props.tag}
          </small>
        </h5>
        <h6 className="ContentInShort">lorem......</h6>
      </div>

      <div className="DraftPostAttr col-sm-2 d-flex flex-column align-items-end justify-content-center">
        <div className="AttrItems ">
          <button className="btn mb-1" onClick={()=>deleteDraft(props.id)}>
            <i className="bi bi-trash"></i>
          </button>
        </div>
      </div>
    </button>
  );
}
