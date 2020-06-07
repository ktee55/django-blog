import {$, $$} from './components/bling.js';
import React from 'react';
import ReactDOM from 'react-dom';
import PhotoInsert from './PhotoInsert';

if (document.querySelector('.photo_insert')) {
  ReactDOM.render(<PhotoInsert />, document.querySelector('.photo_insert'));
}

(function ($, $$) {

  const navbarCollapseFunction = () => {

    let navbarToggler = $('.navbar-toggler-icon')
    let navbarCollapse = $('.navbar-collapse')

    navbarToggler.on('click', function() {
      navbarCollapse.classList.toggle('collapse');
    })

    document.body.on('click', function(e) {
      // if(!e.target.classList.contains('navbar-toggler-icon')) {
      if(e.target !== navbarToggler) {
        navbarCollapse.classList.add('collapse');
      }
    })

  } //navbarCollapseFunction

  navbarCollapseFunction();


  if ($('#id_featured_image')) {
    $('#id_featured_image').on('change', function() {
      let filename = this.value.replace(/^.*[\\\/]/, '')
      $('#label_for_featured_image').innerHTML = filename;
    })
  }


  const multiFormControl = () => {

    // 画像アップロードフォームにて、2番目以降のフォームを隠す（１個だけ表示する）
    const hideOthers = (elem) => {
        let el = document.querySelectorAll(elem);
        for (let i = 1; i < el.length; i++) {
          el[i].classList.add('hide');
          el[0].classList.add('mt-0');
        }
    } // hideOthers

    // hideOthers('link-form'); //Post新規投稿ページ =>下記functionに統一=>
    hideOthers('.photo-form .multiField'); //Photo Upload Page


    // クリックで１個ずつフォームの表示・非表示
    const toggleForms = (elem) => {
      let el = document.querySelectorAll(elem);
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

    // toggleForms('link-form'); //Post新規投稿ページ =>下記functionに統一=>
    toggleForms('.photo-form .multiField'); //Photo Upload Page


    // 既にデータが入ってるフォームのみ表示
    const hideEmptyForms = (elem) => {
      let linkForms = document.querySelectorAll(elem);
      linkForms.forEach(form => {
        // console.log(form.value);
        if ( form.value == "" || form.value == null ) {
          //空のフォームを非表示、表示/非表示をコントロール、"削除する"チェックボックスを非表示にする->SCSS
          form.parentNode.parentNode.parentNode.classList.add('hide', 'togglable', 'url-empty');
        }
      })
      // PostにURLがひとつもない場合(新規投稿含む)、ひとつだけ空のフォームを表示
      let el = document.querySelectorAll('.no-urls .togglable')[0]
      if (el) {
        el.classList.remove('hide');
      }

      toggleForms('.togglable');
    }

    hideEmptyForms('.link-form .urlinput');


  } //multi_form_control

  multiFormControl()


  const modalControl = () => {
    
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
    modalControl();
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