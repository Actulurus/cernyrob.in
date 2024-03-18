document.addEventListener('DOMContentLoaded', function () {
    var quizButtonElement = document.getElementById('answer-button')
    var titleText = document.getElementById("video-name").innerText
    

    const queryString = window.location.search
    const queryParams = new URLSearchParams(queryString)
    const topicSlug = queryParams.get('topic')

    const questionApiPath = window.location.origin + "/kafka/quiz/questions?topic=" + topicSlug
    const topicApiPath = window.location.origin + "/kafka/quiz/info?topic=" + topicSlug
    var questions = []

    fetch(topicApiPath)
        .then(response => response.json())
        .then(data => {
            console.log(data)
           let topic = data["course_name"]
              document.getElementById("video-name").innerText = document.getElementById("video-name").innerText + " " + topic
           console.log(topic)
        })
        .catch(error => {
            console.error('Error:', error);
        });

    fetch(questionApiPath)
        .then(response => response.json())
        .then(data => {
           for (const [question, answer] of Object.entries(data.questions)) {
                questions.push(question)
                console.log(question)
                document.getElementById("quiz-question").innerText = questions[0]
              }

        })
        .catch(error => {
            console.error('Error:', error);
        });





    var userAnswers = []

    let currentQuestionIndex = 0

    function displayQuestion() {
        var questionElement = document.getElementById('quiz-question')
        questionElement.textContent = questions[currentQuestionIndex]
    }

    function checkAnswer(answer) {
        userAnswers.push(answer)
        currentQuestionIndex++
        if (currentQuestionIndex < questions.length) {
            displayQuestion()
            document.getElementById('answer-input').value = ""
        } else {
            console.log(userAnswers)
            let payload = {}
            for (let i = 0; i < questions.length; i++) {
                payload[questions[i]] = userAnswers[i]
            }

            let formData = new FormData()
            formData.append('questions_answers', JSON.stringify(payload))
            formData.append('topic', topicSlug)

            fetch('/kafka/quiz/evaluate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: formData
            })
                .then(response => {
                    if (response.ok) {
                        console.log('Answers submitted successfully');
                    } else {
                        console.error('Failed to submit answers');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });

            document.getElementById("question-container").style.display = "none"
            document.getElementById("user-answer-container").style.display = "none"

            document.getElementById("video-name").innerText = "Dokončil jsi " + titleText;

        }
    }

    quizButtonElement.addEventListener('click', function () {
        var answerInputElement = document.getElementById('answer-input')
        var answer = answerInputElement.value
        checkAnswer(answer)
        console.log(answer)
    })
})

function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}