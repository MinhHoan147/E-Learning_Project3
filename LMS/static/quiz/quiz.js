// console.log('Hello World!');
const url = window.location.href;

const quizBox = document.getElementById('quiz-box');
const answerBox = document.getElementById('answer-box');
const scoreBox = document.getElementById('score-box');
const timerBox = document.getElementById('timer-box');
const buttonBox = document.getElementById('button-box');

const activateTimer = (time) => {
    // console.log(time);

    if (time.toString().length < 2) {
        timerBox.innerHTML += `<h5><b>0${time}:00</b></h5>`;
    } else {
        timerBox.innerHTML += `<h5><b>${time}:00</b></h5>`;
    }
    let minutes = time - 1;
    let seconds = 60;
    let displaySeconds;
    let displayMinutes;
    const timer = setInterval(() => {
        seconds--;
        if (seconds < 0) {
            seconds = 59;
            minutes--;
        } 
        if (minutes.toString().length < 2) {
            displayMinutes = `0${minutes}`;
        } else {
            displayMinutes = minutes;
        }
        if (seconds.toString().length < 2) {
            displaySeconds = `0${seconds}`;
        } else {
            displaySeconds = seconds;
        }

        if (seconds == 0 && minutes == 0) {
            timerBox.innerHTML = `<h5><b>00:00</b></h5>`;
            setTimeout(() => {
                clearInterval(timer);
                alert('Time is up');
                sendData();
            }, 500);

            
        }

        timerBox.innerHTML = `<h5><b>${displayMinutes}:${displaySeconds}</b></h5>`;

    }, 1000);
}
let data;
$.ajax({
    type: 'GET',
    url: `${url}/data`,
    success: function (response) {
        // console.log(response)
        const data = response.data
        data.forEach(element => {
            for (const [question, answer] of Object.entries(element)) {
                quizBox.innerHTML += `
                <hr>
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">${question}</h5>
                    </div>
                </div>
                `
                answer.forEach(ele => {
                    if (ele != null) {
                        quizBox.innerHTML += `
                        <div class="card">
                            <div class="card-body">
                                <input class='ans radio radio-primary' type="radio" name="${question}" id="${question}-${answer}" value="${ele}">
                                <label for="${question}-${answer}">${ele}</label>
                            </div>
                        </div>
                      `
                        
                    }
                }); 
            }
        });
        activateTimer(response.time)
        // back button
        
    },
    error: function (error) {
        console.log(error)
    }
})

const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]

    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(el => {
        if (el.checked) {
            data[el.name] = el.value
        } else {
            if (!data[el.name]) {
                data[el.name] = null
            }
        }
    })

    $.ajax({
        type: 'POST',
        url: `${url}/save`,
        data: data,
        success: function (response) {
            
            const results = response.results
            quizForm.classList.add('not-visible')
            // console.log(response)
            scoreBox.innerHTML = `${response.passed ? 'Congratulation!' : 'Sorry you`re failed'} | Your score is ${response.score}`

            results.forEach(res => {
                const resDiv = document.createElement('div')
                for (const [question, resp] of Object.entries(res)) {
                    
                    resDiv.innerHTML += question
                    const cls = ['container', 'p-3','text-light', 'h3']
                    resDiv.classList.add(...cls)

                    if (res == 'not answered') {
                        resDiv.innerHTML += '- not answered'
                        resDiv.classList.add('bg-danger')
                    }
                    else {
                        const answer = resp['answered']
                        const correct = resp['correct_answer']
                        if (answer == correct) {
                            resDiv.classList.add('bg-success')
                            resDiv.innerHTML += ` answered: ${answer}`
                        } else {
                            resDiv.classList.add('bg-danger')
                            resDiv.innerHTML += ` | answered: ${answer} | correct answer: ${correct}`
                        }
                    }
                }
                answerBox.append(resDiv)
                const url_course = url.split("/");

                buttonBox.innerHTML = `<a href="/" class="btn btn-primary">Back</a>`
                // after 10 seconds redirect to home page
            });
        },
        error: function (error) {
            console.log(error)
        }
    })
}

quizForm.addEventListener('submit', e => {
    e.preventDefault()

    sendData()
})