$(function () {
    const iframe = document.getElementById("view-frame");
    if (iframe) {
        const target = iframe.contentWindow;
        createAnnotationDisplay();

        window.addEventListener("message", (e) => {
            const data = e.data;
            console.log(data);
            if (data.type === 'ready') {
                sendMessage({type: 'ready'});
            } else if (data.type === 'annotation') {
                console.log(data)
                showAnnotation(data.data);
            }
        });

        function showAnnotation(annotation) {
            $('.annotation-title').text(
                annotation['title']
            );

            $('.annotation-image').attr(
                'src',
                annotation['photo']
            );

            $('.annotation-description').text(
                annotation['description']
            );

            $(document.body).addClass('annotation-modal-open');
            $(`#annotation-modal`).css('display', 'block');
        }

        function sendMessage(message) {
            if (target) {
                target.postMessage(JSON.parse(JSON.stringify(message)), '*');
            }
        }

        function createAnnotationDisplay() {
            $(document.body).append(`
                <style>
                .annotation-modal {
                  display: none; 
                  position: fixed;
                  z-index: 1000;
                  padding-top: 100px;
                  left: 0;
                  top: 0;
                  width: 100%;
                  height: 100%;
                  overflow: auto;
                  background-color: rgb(0,0,0);
                  background-color: rgba(0,0,0,0.4);
                }
                .annotation-modal-content {
                  background-color: #fefefe;
                  margin: auto;
                  padding: 20px;
                  border: 1px solid #888;
                  width: 30%;
                }
                .annotation-modal-content .close {
                  color: #aaaaaa;
                  float: right;
                  font-size: 28px;
                  font-weight: bold;
                }
                .annotation-modal-content .close:hover,
                .annotation-modal-content .close:focus {
                  color: #000;
                  text-decoration: none;
                  cursor: pointer;
                }
                </style>
                <div id="annotation-modal" class="annotation-modal">
                  <div class="annotation-modal-content">
                    <span class="close annotation-modal-close">&times;</span>
                    <h4 class="annotation-title" style="text-align: center;padding: 5px;color: black;"></h4>
                    <img class="annotation-image" style="width: 100%;">
                    <h6 class="annotation-description" style="font-size: 15px;padding: 10px;text-align: center;color: black;"></h6>
                  </div>
                </div>
            `);
        }

        window.addEventListener(
            'click',
            function (event) {
                var isAnnotationModal = $('#annotation-modal').length > 0;
                if (
                    isAnnotationModal &&
                    ($(event.target).hasClass('annotation-modal-open') ||
                        $(event.target).hasClass('annotation-modal-header') ||
                        $(event.target).hasClass('annotation-modal-close'))
                ) {
                    event.stopPropagation();
                }

                if ($(event.target).hasClass('annotation-modal-close')) {
                    $(document.body).removeClass('annotation-modal-open');
                    $(`#annotation-modal`).css('display', 'none');
                }
            },
            true
        );

    }
});