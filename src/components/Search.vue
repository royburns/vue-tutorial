<template>
    <div class="card">
        <div class="card-header" align="center">
            <form class="form-inline">
                <input class="form-control form-control-lg wide" v-model="searchKey" type="text" placeholder="搜索公众号/文章">
                <i class="fa fa-search btn btn-lg btn-outline-success" @click="searchMp()"></i>
            </form>
        </div>
        <div class="card-block" v-if="searchData">
            <h5 align="center">共有{{ searchData.totalItems }}条搜索结果，共{{searchData.totalPages}}页</h5>
        </div>
        <div class="card-block">

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
            <div class="media" v-for="(mp,index) in mpResults">
                <div class="media-left imgbox">
                    <a class="" href="#">
                        <img class="media-object rounded " :src="mp.image" style="margin-top: 5px;">
                    </a></div>
                <div class="media-body">
                <a :href="mp.encGzhUrl" target="_blank"><h4 v-html="mp.name"></h4></a>
                    <p class="" style="margin-bottom: 0px;"> 简介：<small v-html="mp.summary"></small></p>
                    <p class="text-muted" style="margin-bottom: 0px;">
                     <a href="javascript:" @click="subscribe(index)">
                            <i class="fa fa-lg float-xs-right text-danger"
                               :class="{'fa-star': mp.isSubscribe, 'fa-star-o': ! mp.isSubscribe,}"></i></a>
                      <small><i class="fa fa-eye"></i> 1181 </small>
                        <small class=" s2"> 最近更新 {{ mp.date }} </small></p>
                        
                 <p class="text-muted" style="margin-bottom: 30px;"> <small class="text-muted s1"> <a :href="mp.url" target="_blank">{{ mp.title1}}</a>
                  <span v-html="mp.content"></span> </small> </p>
  
                </div>
            </div>
        </div>
    </div>
</template>

<style>
    .form-inline .wide {
        width: 80%;
    }
    .imgbox {
        width: 100px;
        height: 140px;
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
                searchKey: '',
                date : '',
                totalTime : '',
                comment : '',
                mpName: '凤凰网',
                isSubscribe: false,
                myData: '',
                searchData: '',
                searchMpXml: '',
                mpResults: []
            }
        },
        computed : {
            mpList() {
                // 从store中取出数据
                return this.$store.state.mpList
            }
        },
        methods:{
            searchMp() {
                this.$http.jsonp("http://weixin.sogou.com/weixinwap?_rtype=json&ie=utf8&type=1",
                    {
                        params: {
                            page: 1,
                            type: 1, //公众号
                            query: this.searchKey
                        },
                        jsonp:'cb'
                    }).then(function(res){
                    this.myData = JSON.parse(res.bodyText).totalItems;
   //                 console.log(this.myData);
                    this.searchData = JSON.parse(res.bodyText);
                    var mpXmls = this.searchData.items;
                     var i, xmlDoc, mpResult;
                    for (i in mpXmls) {
                   	mpResult = {}
                                 xmlDoc = new DOMParser().parseFromString(mpXmls[i], 'text/xml');
 			mpResult['title'] = xmlDoc.getElementsByTagName("title")[1].childNodes[0].nodeValue; 
			mpResult['name'] = xmlDoc.getElementsByTagName("name")[0].childNodes[0].nodeValue.replace('', '<span class="text-success">').replace('', '</span>'); 
			mpResult['summary'] = xmlDoc.getElementsByTagName("summary")[0].childNodes[0].nodeValue.replace('', '<span class="text-success">').replace('', '</span>'); 
			mpResult['encGzhUrl'] = xmlDoc.getElementsByTagName("encGzhUrl")[0].childNodes[0].nodeValue; 	// 主页链接
			try 	{ 
				mpResult['url'] = xmlDoc.getElementsByTagName("url")[2].childNodes[0].nodeValue; 		// 最新更新文章
				mpResult['title1'] = xmlDoc.getElementsByTagName("title1")[0].childNodes[0].nodeValue; 
			} 
			catch (e) 	{ 
				mpResult['url'] =  '';
				mpResult['title1'] =  ''
			} 
			try 	{ 
			mpResult['content'] = xmlDoc.getElementsByTagName("content")[0].childNodes[0].nodeValue.replace('', '<span class="text-success">').replace('', '</span>'); 
			} 
			catch (e) 	{ 
				mpResult['content'] = ''
			} 
  			
 			mpResult['date'] = xmlDoc.getElementsByTagName("date")[1].childNodes[0].nodeValue; 
            		mpResult['image'] = xmlDoc.getElementsByTagName("image")[0].childNodes[0].nodeValue; 	
            		mpResult['weixinhao'] = xmlDoc.getElementsByTagName("weixinhao")[0].childNodes[0].nodeValue; 	
            		mpResult['isSubscribe'] = false;
                    	this.mpResults.push(mpResult);	
                    }
                    this.searchKey = ''
                },function(){
                    console.log('searchMp error')
                });
            },
//                axios.jsonp('http://weixin.sogou.com/weixinwap?page=1&_rtype=json&ie=utf8&type=1&query=' + this.searchKey)
//                    .then(function (response) {
//                        console.log(response);
//                        this.searchKey = '';
//                    })
//                    .catch(function (error) {
//                        console.log(error);
//                    });
//                    this.refreshing = true;
//                    this.$nextTick(function () {    //异步更新队列: 可以在数据变化之后立即更新 DOM
//                        this.refreshing = true;
//                        console.log('now is loading:'+this.refreshing) // => 'updated'
//                    });
//                    var self = this;
//                    getJSON('/api/refresh/' + this.table, {
//                    }, function (err, data) {
//                        self.last_update = data.last_update;
//                        self.lz_update = data.lz_update;
//                        self.refreshing = false;   // 隐藏 refreshing
//                        self.msg = data.msg;
//                        this.$nextTick(function () { });
//
//                    });


            subscribe(idx) {
  	if (this.mpResults[idx].isSubscribe== true ) {
  	               // 删除该公众号
                 this.mpResults[idx].isSubscribe = false;
                return this.$store.dispatch('unsubscribeMp', '', this.mpResults[idx].weixinhao)
            };
            
                var mp = {
                    mpName : this.mpResults[idx].title,
                    image : this.mpResults[idx].image,
                    date : this.mpResults[idx].date,
                    weixinhao : this.mpResults[idx].weixinhao,
                    subscribeDate : new Date().getTime()
                };
                for(let item of this.mpList) {
                    if(item.mpName == mp.mpName) return false
                }
                this.$store.dispatch('subscribeMp', mp);
                this.mpResults[idx].isSubscribe = true;
//                this.$store.dispatch('addTotalTime', this.totalTime);
//                this.$router.go(-1)
            }
        }
    }
</script>
