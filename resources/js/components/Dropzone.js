import React, {Component} from 'react'
import Dropzone from 'react-dropzone'

class MyDropzone extends Component {

  constructor() {
    super();
    this.onDrop = (files) => {
      // this.setState({files})
      // this.setState({ description: files[0].name})
      this.props.dropChange(files[0])
    };
    // this.state = {
    //   // files: [],
    //   description: "画像ファイルをここにドラッグ＆ドロップするか、クリックしてファイルを選んで下さい。"
    // };
  }
  
  render() {
    // const files = this.state.files.map(file => (
    //   <li key={file.name}>
    //     {file.name} - {file.size} bytes
    //   </li>
    // ));

    return (
      <Dropzone onDrop={this.onDrop}>
        {({getRootProps, getInputProps}) => (
        <section className="dropzone-container">
          <div {...getRootProps({className: 'dropzone keep-modal'})}>
            <input {...getInputProps()} type="file" className="keep-modal"/>
            <small className="keep-modal">{this.props.description}</small>
          </div>
          {/* <aside>
            <ul>{files}</ul>
          </aside> */}
        </section>
        )}
      </Dropzone>
    );
  }
}

export default MyDropzone;


// import React from 'react';
// import {useDropzone} from 'react-dropzone';

// function MyDropzone(props) {
//   const {acceptedFiles, getRootProps, getInputProps} = useDropzone({
//     onDrop:  acceptedFiles => {
//       document.querySelector('.dropzone p').innerHTML({files})
//       props.dropChange(acceptedFiles[0])
//     }
//   });
  
//   const files = acceptedFiles.map(file => (
//     <li key={file.path}>
//       {file.path} - {file.size} bytes
//     </li>
//   ));

//   return (
//     <section className="dropzone-container">
//       <div {...getRootProps({className: 'dropzone keep-modal'})}>
//         <input {...getInputProps()} className="keep-modal"/>
//         <p className="keep-modal">画像ファイルをここにドラッグ＆ドロップするか、クリックしてファイルを選んで下さい。</p>
//       </div>
//       <aside>
//         <ul>{files}</ul>
//       </aside>
//     </section>
//   );
// }

// export default MyDropzone;