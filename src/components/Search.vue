<template>
    <div class="card">
        <div class="card-header" align="center">
            <form class="form-inline">
                <input class="form-control form-control-lg wide" v-model="searchKey" type="text" placeholder="搜索公众号/文章">
                <i class="fa fa-search btn btn-lg btn-outline-success" @click="searchMp()"></i>
            </form>
        </div>
        <div class="card-block" id="searchResult1">
            <div class="media">
                <div class="media-left imgbox">
                    <a class="" href="#">
                        <img class="media-object rounded"
                             src="http://dl.bizhi.sogou.com/images/2014/04/22/587880.jpg">
                    </a></div>
                <div class="media-body">

                    <h4>这个导演的新片，每一部我必二刷</h4>
                    <p class="text-muted" style="margin-bottom: 0px;">
                        11月的时候，鱼叔采访了自己的偶像——蒂姆·波顿。并有机会提前看到了他的新片，然后写了一篇推文。今天电影上映，鱼叔去电影院二刷。这一次，又
                    </p>
                    <p><small class="text-muted s1">
                        <span @click="subscribe()"><i class="fa fa-star-o fa-lg float-xs-right text-danger"></i></span>
                        <i class="fa fa-eye"></i> 2348 </small>
                        <small class="text-muted"> 	独立鱼电影</small>
                        <small class="text-muted s2"> 1小时前</small>
                    </p>
                </div>
            </div>
            <div class="media" id="searchResult2">
                <div class="media-left imgbox">
                    <a class="" href="#">
                        <img class="media-object rounded "
                             src="http://wx.qlogo.cn/mmhead/Q3auHgzwzM6FDWDyWSNm2AFBwFV6SFMXa20hjbFlWOyGYFQqrryIPw/0">
                    </a></div>
                <div class="media-body">

                    <h4>现在的段子，不动脑子根本就看不懂</h4>
                    <p class="text-muted" style="margin-bottom: 0px;">
                        周末，姑妈让我帮忙表照顾5岁的表弟，晚上我给他洗澡的时候，女票打来电话。因为手不方便拿，就开了免提，她问:在做什么呢？我说...
                    </p>
                    <p><small class="text-muted s1">
                        <a href="javascript:" @click="subscribe()">
                            <i class="fa fa-lg float-xs-right text-danger"
                               :class="{'fa-star': isSubscribe, 'fa-star-o': !isSubscribe,}"></i></a>
                        <i class="fa fa-eye"></i> 1181 </small>
                        <small class="text-muted s1">凤凰网</small>
                        <small class="text-muted s2"> 3小时前</small>
                    </p>
                </div>
            </div>
            <!--<a class="list-group-item" v-for="(plan,index) in plans">-->
        </div>
    </div>
</template>

<style>
    .form-inline .wide {
        width: 80%;
    }
    .imgbox {
        width: 100px;
        height: 120px;
        overflow: hidden;
    }
    .imgbox img{
        max-width: 100px;
        /*max-height: 120px;*/
    }
    .s1 {
        margin-right: 20px;
    }
    .s2 {
        margin-left: 20px;
    }
</style>

<script>
    export default {
        name : 'SearchResult',
        data() {
            return {
                searchkey: '',
                date : '',
                totalTime : '',
                comment : '',
                mpName: '凤凰网',
                isSubscribe: false
            }
        },
        computed : {
            mpList () {
                // 从store中取出数据
                return this.$store.state.mpList
            }
        },
        methods:{
            searchMp() {
              alert(this.searchKey);
            },
            subscribe() {
                const mp = {
                    mpName : this.mpName,
                    image : 'https://sfault-avatar.b0.upaiyun.com/888/223/888223038-5646dbc28d530_huge256',
                    date : this.date,
                    totalTime : this.totalTime,
                    comment : this.comment
                };
                for(let item of this.mpList) {
                    if(item.mpName == mp.mpName) return false
                }
                this.$store.dispatch('subscribeMp', mp);
                this.isSubscribe = true;
//                this.$store.dispatch('addTotalTime', this.totalTime);
//                this.$router.go(-1)
            }
        }
    }
</script>
