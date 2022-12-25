<script>
    import json from '../../../data/MovieData.json'
    export default{
        data(){
            return{
                imdb: json["imdb"],
                title: json["imdb"]["title"],
                website: json["imdb"]["website"],
                second_name: json["imdb"]["second_name"],
                original_name: json["imdb"]["origin_name"],
                is_series: json["imdb"]["is_series"],
                year: json["imdb"]["year"],
                length: json["imdb"]["length"],
                hashtags: json["imdb"]["hashtags"],
                poster_url: json["imdb"]["poster"],
                director: json["imdb"]["director"],
                actors: json["imdb"]["actors"],
                intro: json["imdb"]["intro"],
                score: json["imdb"]["score"],
                vote_num: json["imdb"]["vote_num"],
                comment_url: json["imdb"]["comment_url"],
                all_comments: json["imdb"]["all_comments"],
                NLP_score: json["imdb"]["NLP Score"],
            }
        }
    }
</script>
<template >
    <!-- <main class="bg"> -->
        <div>
            <div class ="header">
                <img :src=poster_url width="210" />
                <div class="titlebox">
                    <!-- <div class="title">Title: {{title}}</div> -->
                    <div class="title">Title : {{title}}</div>
                    <!-- <div class="title">website : {{ website }}</div> -->
                </div>
            </div>
            <div class="text">              
                <!-- <div>Is_movie : {{is_movie?'⭕':'❌'}}</div> -->
                <!-- <div>Is_series : {{is_series?'⭕':'❌'}}</div> -->
                <div >Hashtags : 
                    <div v-for ="hashtag in hashtags" class="hashtagbox">
                        #{{hashtag}}
                    </div >
                </div>
                <!-- <div>Release date : {{date}}</div> -->
                <div>Release year : {{year}}</div>
                <div>Length : {{length}}</div>
                <div>Director : {{director}}</div>
                <div>Actors :
                    <div v-for ="actor in actors" class ="actorbox"> 
                        {{actor}}
                    </div>
                </div>
                <div>Website Score : {{score}}/10</div>
                <div>Vote Turnout : {{vote_num}}</div>
                <!-- <div>Comment_url : {{comment_url}}</div> -->
                <div>NLP_score : {{ NLP_score }}
                    <!-- {{"en_score : "+NLP_score["en_score"]}}
                    {{"zh_score : "+NLP_score["zh_score"]}}
                    {{ "all_score : "+ NLP_score["all_score"] }} -->
                </div>
                <div >Intro : 
                    <div class="introbox">
                    {{intro}}
                    </div>
                </div>
                <!-- <div>Age restriction : {{rating}}+</div> -->
                <!-- <div>poster_url: {{poster_url}}</div> -->
                <div>All_comments : 
                    <div v-for ="(comment,i) in all_comments" class = "commentbox">
                        {{ i+1 +". "}}
                        {{"👤 : "+comment.text}}
                    </div>
                </div>
            </div>
        </div>
    <!-- </main> -->
</template>
<style scoped>
.hashtagbox{
    display: inline-block;
    /* background-color: rgb(24, 38, 50); */
    /* padding: 10px; */
    /* left:100px; */
    /* top: -200px; */
}
.actorbox{
    /* display: inline-block; */
    /* background-color: rgb(24, 38, 50); */
    padding: 3px;
    left:50px;
    /* top: -200px; */
}
.commentbox{
    /* display: inline-block; */
    /* background-color: rgb(24, 38, 50); */
    padding: 10px;
    /* left:50px; */
    /* top: -200px; */
}
.introbox{
    /* display: inline-block; */
    /* background-color: rgb(24, 38, 50); */
    padding: 10px;
    /* left:50px; */
    /* top: -200px; */
}
.text {
    /* top: 20px; */
    font-size: 20px;
    padding: 10px;
    /* left: 500px; */
    /* border: 3px solid #73AD21; */
    /* float: right; */
    /* width: 1300px; */
}
.titlebox{
    display: inline-block;
    background-color: rgb(24, 38, 50);
    padding: 10px;
    left:100px;

    /* top: -200px; */
}
.title{
    font-size: 30px;
    font-weight: bold;
    /* float: right; */
}
.header {
    /* display: inline-block; */
    background-color: rgb(24, 38, 50);
    /* border: 2px solid aliceblue; */
    padding: 10px;
    width: 1300px;
    /* float: left; */
    /* width: all; */
    /* height: all; */
}


</style>