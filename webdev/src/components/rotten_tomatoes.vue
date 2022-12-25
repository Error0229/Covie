<script>
    import json from '../../../data/MovieData.json'
    export default{
        data(){
            return{
                rotten_tomatoes: json["rotten_tomatoes"],
                title: json["rotten_tomatoes"]["title"],
                // en_name: json["rotten_tomatoes"]["en_name"],
                // zh_name: json["rotten_tomatoes"]["zh_name"],
                hashtags: json["rotten_tomatoes"]["hashtags"],
                date: json["rotten_tomatoes"]["date"],
                year: json["rotten_tomatoes"]["year"],
                length: json["rotten_tomatoes"]["length"],
                director: json["rotten_tomatoes"]["director"],
                actors: json["rotten_tomatoes"]["actors"],
                tomatoscore: json["rotten_tomatoes"]["rating"],
                tomato_num: json["rotten_tomatoes"]["rating_count"],
                score: json["rotten_tomatoes"]["audience_rating"],
                vote_num: json["rotten_tomatoes"]["audience_rating_count"],
                comment_url: json["rotten_tomatoes"]["comment_url"],
                intro: json["rotten_tomatoes"]["intro"],
                // rating: json["yahoo"]["rating"],
                poster_url: json["rotten_tomatoes"]["poster"],
                all_comments: json["rotten_tomatoes"]["all_comments"],
                NLP_score: json["rotten_tomatoes"]["NLP Score"],
                

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
                <div>Release data : {{date}}</div>
                <div>Length : {{length}}</div>
                <div>Director : {{director}}</div>
                <div>Actors :
                    <div v-for ="actor in actors" class ="actorbox"> 
                        {{actor}}
                    </div>
                </div>
                <div>Rotten Tomatoes : {{tomatoscore}}%/100%</div>
                <div>Rotten Tomatoes Vote Turnout : {{ tomato_num }}</div>
                <div>Audience Score : {{score}}%/100%</div>
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