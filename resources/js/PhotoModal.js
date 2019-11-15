import React from 'react'
import PhotoInsert from './PhotoInsert';

class PhotoModal extends React.Component {

  constructor(props){
    super(props)
    this.state = {
      isShow: false,
      isTop: false
    }
  }

  showModalA = () => {
    this.setState({ isTop: true, isShow: true }) 
  }

  showModalB = () => {
    this.setState({ isTop: false, isShow: true }) 
  }

  closeModal = (e) => {
    if(!e.target.classList.contains('keep-modal')) {
       this.setState({ isShow: false }) 
    }
  }

  shutdownModal = () => {
    this.setState({ isShow: false }) 
  }

  render() {
    return (
      <div>
        <a id="insert-top-image" className="btn btn-outline-info btn-sm mt-1 mb-1" onClick={this.showModalA}>トップ画像を挿入</a>
        <a id="insert-image-into-content" className="btn btn-outline-info btn-sm mt-1 mb-1" onClick={this.showModalB}>投稿に画像を挿入</a>
            { this.state.isShow && <PhotoInsert 
              closeModal={this.closeModal}
              shutdownModal={this.shutdownModal}
              isTop={this.state.isTop}
            /> }
      </div>
     )
  }

}

export default PhotoModal;