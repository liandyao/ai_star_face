/**
 * 
 * @param {*} urlType 
 * @param {接口请求地址} url 
 * @param {接口请求类型} type 
 * @param {接口请求参数} date 
 * @param {接口请求头的携带信息，如不自定将某人携带token为请求头部} header 
 * @param (status === 0 为接口请求失败返回失败原因，并弹框展示) 
 * @param (status === 1 为接口请求成功返回成功响应数据) 
 * @param (status === 2 为接口请求成功，但是需要token校验，没有token返回登录页面重新授权登录回去token)
 *
 *
 */

let baseURL = 'http://127.0.0.1:8080/socials' //此处改成自己的域名
 	
	
if(process.env.NODE_ENV === 'development'){
	baseURL='https://caineng.com/mym';
}else{
	baseURL='https://caineng.com/mym';
} 

/*所有api的路径统一管理*/
const apiPath = {
	common: {
		feedback: baseURL+'/school_api/index/feedback' , // 反馈建议
		shareUser: baseURL+'/school_api/index/shareUser' , // 分享加分
		userSurplus: baseURL+'/school_api/index/userSurplus' , // 查询积分
		makePhoto: baseURL+'/school_api/index/makePhoto'  ,// 制作照片(扣分),
		videoPlus: baseURL+'/school_api/index/videoPlus' , // 看广告视频加分
	},
	user: {
		//微信小程序登录
		miniAppLogin: baseURL+'/school_api/wxuser/login', 
		//微信小程序登录,已经获取过openid
		miniAppLoginOpenid: baseURL+'/school_api/wxuser/loginByOpenid', 
		//登出
		logout: baseURL+'/school_api/baseUser/logout',
		
		//我的分享历史记录
		myShare: baseURL + '/school_api/baseUser/myShare'
	}
};


// 未获取token跳转的授权页面
const indexUrl = '/pages/index/index'
 
// 接口请求提示语句
const msg = '请稍候...'

// 明星撞脸appid
let miniAppid = 'wx97a2857166ff17b7'
 

const request = (urlType= '', url = '', type = '', data = {}, header = {}) => {
	var that = this
	if(JSON.stringify(header)=='{}'){ 
		header={
			'Content-type': 'application/json',
			'sstoken': uni.getStorageSync('tokenValue')			
		}
	}
	//始终加入对方的openid,可以判断用户是否违规使用
	let openid = uni.getStorageSync("openid");
	if(openid){
		if(!data){
			data = {}
		}
		data.openid = openid;
		// app名称
		data.appName = 'star_face';
	}
	
    return new Promise((resolve, reject) => {
		
		//console.info(url+"  "+type+"  "+data)
        uni.request({
            method: type,
            url: url,
            data: data,
            header: header,
            dataType: 'json'         
        }).then((response) => {
			console.log(response)
			// uni.hideLoading();
			if (response[1].data.code == 200) {
				let [error, res] = response;
				 
				resolve(res.data);
			} else if (response[1].data.code == 401) {
				uni.showToast({
				    title: '请先登录',
					icon: 'error',
				    duration: 2000,
					success: () => {
					}
				});
				reject(response[1].data)
				
				uni.switchTab({
					url:indexUrl
				})
				
			}  else if (response[1].statusCode == 403) {
				uni.showToast({
				    title: '请先登录',
					icon: 'error',
				    duration: 2000,
					success: () => {
					}
				});
				uni.clearStorage();
				resolve(response[1].data)
				
			} else if(response[1].data.code == 500){
				uni.showToast({
				    title: '系统错误,请联系管理员!',
					icon: 'error',
				    duration: 2000,
					success: () => {
					}
				});
				resolve(response[1].data)
			}
        }).catch(error => {
            let [err, res] = error;
            reject(err)
			console.log(error[1].data)
			uni.showToast({
			    title: error,
				icon: 'none',
			    duration: 2000
			});
        })
    });
	
}

//post请求
const post= (url = '',  data = {})=>{
	
	let method = 'POST';
	return new Promise((resolve, reject) => {
		console.info('===>',url);
		
		request('',url, method, data).then(res=>{
			resolve(res)
		},err=>{
			reject(res)
		}).catch(error => {
            let [err, res] = error;
            reject(err) 
			uni.showToast({
			    title: error,
				icon: 'none',
			    duration: 2000
			});
        });
	
	})
	 
}

const get= (url = '',  data = {})=>{
	
	let method = 'GET';
	return new Promise((resolve, reject) => {
		
		 request('',url, method, data).then(res=>{
			resolve(res)
		},err=>{
			reject(res)
		});
	
	})
	 
}



/*无状态提示信息*/
const alert = function(msg = '', icon = 'none', url = '', openType = 'navigate') {
	/*消息强制转字符串*/
	if (typeof(msg) != 'string') {
		msg = msg.toString();
	}

	if (msg.length > 7) {
		//长度超过7个字符，用示模态弹窗展示
		uni.showModal({
			title: '提示',
			content: msg,
			showCancel: false
		});
	} else {
		if (icon == 'warning') {
			uni.showToast({
				title: msg,
				image: "/static/images/icon-warning.png"
			});
		} else {
			uni.showToast({
				title: msg,
				icon: icon
			})
		}
	}
	if (url || openType == 'back') {
		setTimeout(() => {
			if (openType == 'redirect') {
				uni.redirectTo({
					url: url
				});
			} else if (openType == 'switchTab') {
				uni.switchTab({
					url: url
				});
			} else if (openType == 'reLaunch') {
				uni.reLaunch({
					url: url
				});
			} else if (openType == 'back') {
				uni.navigateBack();
			} else {
				uni.navigateTo({
					url: url
				});
			}
		}, 1500)
	}
};

//微信小程序登录
const miniAppLogin = function(){
	
	// #ifdef MP-WEIXIN
	
	return new Promise((resolve, reject) => {
		let openid = uni.getStorageSync("openid");
		//如果已经登录过
		if(openid){
			post(apiPath.user.miniAppLoginOpenid+'?openid='+openid).then(res=>{
				loginToken(res.data);//登录
				resolve(res);
			}).catch(err => {
				reject(err);
			})
			
		}else{
			uni.login({
			  provider: 'weixin', //使用微信登录
			  success: function (loginRes) {
			    console.log('loginRes',loginRes);
				//登录
				let data = {
					appid:miniAppid,
					code: loginRes.code
				}
				post(apiPath.user.miniAppLogin,data).then(res=>{
					loginToken(res.data);//登录
					resolve(res);
				}).catch(err => {
					reject(err);
				})
			  },
			  fail: function(err) {
			  	reject(err);
			  }
			});
		}
	});
	
	// #endif
	
	// #ifndef MP-WEIXIN
	return Promise.resolve();
	// #endif
}

//登录
const loginToken = function(res){
	if(res){
		uni.setStorageSync("tokenName",res.tokenName);
		uni.setStorageSync("tokenValue",res.tokenValue);
		uni.setStorageSync("openid",res.openid);
		uni.setStorageSync("isLogin",1);
		uni.setStorageSync("userInfo",res.userInfo)
		//分享时需要
		uni.setStorageSync("mySelfShareId",res.userInfo.id)
	}
	
}

//登出,注销
const logout=function(){
	uni.clearStorageSync()
	post(apiPath.user.logout).then(res=>{
		if(res.code==200){
			alert('登出成功');
		}
	})
}

export default {
	request,post,apiPath,get,alert,miniAppLogin,logout
}
