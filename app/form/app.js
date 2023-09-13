const url ='http://127.0.0.1:8000/api/loansrequest';
const formList = document.querySelector('.form-list');
const loadingElement = document.querySelector('#loading')
const loadedElement = document.querySelector('#loaded')
const loanForm = document.querySelector('.loan-form')
const alert = document.querySelector('.alert');
const modalPlace = document.querySelector(".modal-placeholder");


window.addEventListener('load', function() {
    async function getFormFields(){
        const response =  await fetch(url);
        const data = await response.json();
        loadingElement.classList.add('hide')
        formList.innerHTML = data.data;
    }
    getFormFields();
});

// Post a loan request
async function postLoanRequest(loanRequest){
    const response = await fetch(url, {
        method: "POST",
        body: loanRequest,
        headers: {
            "content-type": "application/json",
        },

    })
    .then(function(data){
        if (!data.ok){
            displayAlert('solicitação falhou', 'danger');
        }
        else{            
            displayAlert('solicitação realizada com sucesso', 'success');
            addModalContainer();
        }
        });
    const data = await response.json()

}

// listeners
loanForm.addEventListener('submit', (e) => {
    e.preventDefault();
    let request = {};
    inputs = document.querySelectorAll('input');
    inputs.forEach(function(input) {
        request[input.name] = input.value;
    });
    request = JSON.stringify(request);
    postLoanRequest(request)  
    });

// closeBtn.addEventListener("click", function () {
//     removeModalContainer();
//     });


// display alert
function displayAlert(text, action){
    //show alert
    alert.textContent = text;
    alert.classList.add(`alert-${action}`);
    
    //remove alert
    setTimeout(function(){
        alert.textContent = '';
        alert.classList.remove(`alert-${action}`);
    }, 5000);
}

// modal container
function addModalContainer(){
    modalPlace.classList.add('modal-overlay');
    modalPlace.innerHTML = `<div class="modal-container">
    <p>Solicitação realizada com sucesso. Em breve</p>
    <button class="close-btn"><i class="fas fa-times"></i></button>
  </div>`;
    const closeBtn = document.querySelector(".close-btn");
    closeBtn.addEventListener("click", function () {
        removeModalContainer();
    });
    loanForm.reset()
}

function removeModalContainer(){
    modalPlace.classList.remove('modal-overlay');
    modalPlace.innerHTML = ``
}