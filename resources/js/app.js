import {$, $$} from './components/bling.js';
import React from 'react';
import ReactDOM from 'react-dom';
import PhotoInsert from './PhotoInsert';

if (document.querySelector('.photo_insert')) {
  ReactDOM.render(<PhotoInsert />, document.querySelector('.photo_insert'));
}

(function ($, $$) {

  $('.navbar-toggler').on('click', function() {
    $('#navbarToggle').classList.toggle('collapse');
  })

  const multi_form_control = () => {

    // 2番目以降のフォームを隠す（１個だけ表示する）
    const hideOthers = (elem) => {
        let el = document.getElementsByClassName(elem);
        for (let i = 1; i < el.length; i++) {
          el[i].classList.add('hide');
          el[0].classList.add('mt-0');
        }
    } // hideOthers

    hideOthers('link-form'); //Post新規投稿ページ
    hideOthers('multiField'); //Photo Upload Page

    // クリックで１個ずつフォームの表示・非表示
    const toggleForms = (elem) => {
      let el = document.getElementsByClassName(elem);
      let i = 1;
      if ($('#add-form')) {
        $('#add-form').on('click', function(e) {
          e.preventDefault();
          el[i].classList.remove('hide');
          i++;
        })
      } 

      if ($('#remove-form')) {
        $('#remove-form').on('click', function(e) {
          i>1 ? i-- : i;
          e.preventDefault();
          el[i].classList.add('hide');
        })
      }
    } // toggleForms

    toggleForms('link-form'); //Post新規投稿ページ
    toggleForms('multiField'); //Photo Upload Page

    // Post更新ページにて既にデータが入ってるフォームのみ表示
    let linkForms = document.querySelectorAll('.link-form-edit .urlinput');
    linkForms.forEach(form => {
      // console.log(form.value);
      if ( form.value == "" || form.value == null ) {
        // console.log('hello');
        form.parentNode.parentNode.parentNode.classList.add('hide', 'togglable');
      }
    })
    // 空のフォームは表示・非表示をコントロールできるように
    toggleForms('togglable');

  } //multi_form_control

  multi_form_control()

  const modal_control = () => {
    
    let modal = $('.modal');

    function expandModal() {
      modal.classList.add('show-modal');
    }

    function closeModal(e) {
      if(!e.target.classList.contains('keep-modal')) {
        modal.classList.remove('show-modal');
      }
    }

    if($('#expand-modal')) {
      $('#expand-modal').on('click', expandModal);
    }

    modal.on('click', closeModal);


  } // modal_control

  if($('.modal')) {
    modal_control();
  }


  // // Without bing.js
  // let modal = document.querySelector('.modal');
  // let photos = document.querySelectorAll('#photos img');

  // function insertImage() {
  //   let image = '<a href="' + this.dataset.origin + '"><img src="' + this.dataset.medium + '"></a>';
  //   document.querySelector('#id_content').value += image;
  // }

  // function expandModal() {
  //   modal.classList.add('show');
  // }

  // function closeModal(e) {
  //   // console.log(e);
  //   // if(e.target==='form') return;
  //   modal.classList.remove('show');
  // }

  // photos.forEach( photo => photo.addEventListener('click', insertImage));

  // document.querySelector('#expand-modal').addEventListener('click', expandModal);

  // modal.addEventListener('click', closeModal);

})($, $$);