const url ='http://127.0.0.1:8000/api/formsettings';
const formList = document.querySelector('.form-list');
const loadingElement = document.querySelector('#loading')
const loadedElement = document.querySelector('#loaded')
const loanForm = document.querySelector('.loan-form')
const alert = document.querySelector('.alert');

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
    const urlPost = "http://127.0.0.1:8000/api/loansrequest"
    const response = await fetch(urlPost, {
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
        }
        });
    const data = await response.json()

}

loanForm.addEventListener('submit', (e) => {
    e.preventDefault();
    let request = {};
    inputs = document.querySelectorAll('input');
    inputs.forEach(function(input) {
        request[input.name] = input.value;
    });
    request = JSON.stringify(request);
    postLoanRequest(request)
    // .then(function(data){
    //     if (!data.ok){
    //         displayAlert('solicitação realizada com sucesso', 'danger');
    //     }
    //     else{
    //         displayAlert('solicitação realizada com sucesso', 'success');
    //     }
    //     });     
    });


// display alert
function displayAlert(text, action){
    alert.textContent = text;
    alert.classList.add(`alert-${action}`);
    
    //remove alert
    setTimeout(function(){
        alert.textContent = '';
        alert.classList.remove(`alert-${action}`);
    }, 1000);

}