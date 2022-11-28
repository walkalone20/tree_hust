export default function ItemListBar(props) {
  return (
    <div className="ItemListBar container d-flex justify-content-between">
      <div className="BarLeft col-md-2">
        <select class="form-select">
          <option>1</option>
          <option>2</option>
          <option>3</option>
          <option>4</option>
        </select>
      </div>
      <div className="BarRight col-md-2 ms-auto d-flex justify-content-center">
        <button className="btn btn-outline-light text-dark">
          <i className="bi bi-check-lg"></i>check
        </button>
      </div>
    </div>
  );
}
