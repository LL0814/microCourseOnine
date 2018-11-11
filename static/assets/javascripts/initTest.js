<script>
        //加载页面，是否已赞
        window.onload = function() {
            let test = {{ test | safe }};
            let ownername = test.ownername;
            let tasks = test.tasks;
            let title = test.title;
            console.log(test);
        }
    </script>