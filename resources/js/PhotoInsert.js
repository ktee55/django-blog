import React from 'react'
import axios from 'axios';

import Dropzone from './components/Dropzone';
import PhotoList from './components/PhotoList';

class PhotoInsert extends React.Component {

  constructor(props){
    super(props)
    this.state = {
      photos: [],
      file: null,
      currentPage: 1,
      setPerPage: 10,
      loading: false,
      description: "画像ファイルをここにドラッグ＆ドロップするか、クリックしてファイルを選んで下さい。"
    }
  }

  getData = () => {
    axios.get('/api/photos/')
      .then(res => {
        // console.log(res.data)
        this.setState({
          photos: res.data
        });
        // console.log(res.data);
      });
  }

  componentDidMount() {
    this.getData();
  }

  addPhoto = (newPhoto) => {
    // console.log(newPhoto)
    this.setState(state => ({
      photos: [newPhoto, ...state.photos]
    }));
  }

  insertImage = (data) => {
    // console.log(e.target.dataset.medium)
    let image = `<a href="${data.origin}"><img src="${data.medium}"></a>`;
    document.querySelector('#id_content').value += image;
  }

  fileUpload = (file) => {
    const url = '/api/photos/';
    const formData = new FormData();
    formData.append('origin', file);
    const config = {
        headers: {
            'content-type': 'multipart/form-data'
        }
    }
    this.setState({
      loading: true
    });
    return axios.post(url, formData, config);
  }

  postData = (e) => {
    e.preventDefault();
    if(this.state.file){
      // this.fileUpload(this.state.file).then(this.getData());
      this.fileUpload(this.state.file).then( res => {
        this.addPhoto(res.data);
        this.setState({
          loading: false,
          description: "画像ファイルをここにドラッグ＆ドロップするか、クリックしてファイルを選んで下さい。"
        });
        // this.insertImage(res.data);
      });
    }
  }

  // onChange = (e) => {
  //   // console.log(e.target.files[0]);
  //   this.setState({file:e.target.files[0]});
  // }

  dropChange = (file) => {
    // console.log(file);
    this.setState({
      file: file,
      description: file.name
    })
  }

  // showList = () => {
  //   document.querySelector('.photo-upload').style.display = 'none';
  //   document.querySelector('.photo-list').style.display = 'block';
  // }

  render() {
    return (
      <div className="modal">
        <div className="wrapper">
          <div className="photo-upload">
            <Dropzone dropChange={this.dropChange} description={this.state.description}/>
            <button className="btn btn-primary keep-modal" onClick={this.postData}>画像をアップロード</button>
            {/* <button className="btn btn-outline-info keep-modal" onClick={this.showList}>アルバムから選択して挿入</button> */}
            {this.state.loading && 
            <button className="btn btn-warning loading" type="button" disabled>
              <span className="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
              Loading...
            </button>
            }
          </div>
          <PhotoList photos={this.state.photos}/>
          {/* <input type="file" className="keep-modal" onChange={this.onChange} />
          <button className="btn btn-primary keep-modal" onClick={this.postData}>アップロード</button> */}
          {/* <form method="POST" action="http://127.0.0.1:8000/api/photos/" onSubmit={this.postData}>
            <input type="file" className="keep-modal" onChange={this.onChange} />
            <button className="btn btn-primary keep-modal" type="submit">アップロード</button>
          </form> */}
        </div>
    </div>
    )
  } //render

}

export default PhotoInsert;
