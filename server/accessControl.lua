local redis_module = require "resty.netcontrol.redisConn";
local ret_unauth_err  = '认证过期，请点击<font color="#FF0000">【右上角插件】</font>重新登陆！'
local ret_auth_err  = '请点击<font color="#FF0000">【右上角插件】</font>登陆认证！'
local template_content = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7"><title>哎呀…您访问的页面不存在-闪送</title><link rel="stylesheet" type="text/css"><style>*{margin:0;padding:0}body{font-family:"微软雅黑";background:#dad9d7}img{border:none}a *{cursor:pointer}li,ul{list-style:none}a{text-decoration:none;outline:0}a:hover{text-decoration:underline}.bg{width:100%%;background:url(https://apkhouse.oss-cn-beijing.aliyuncs.com/vpn/404_01.png) no-repeat center top #dad9d7;position:absolute;top:0;left:0;height:600px;overflow:hidden}.cont{margin:0 auto;width:500px;line-height:20px}.c1{height:360px;text-align:center}.c1 .img1{margin-top:180px}.c1 .img2{margin-top:165px}.c2 .img3{width:24px;height:auto;vertical-align:middle}.cont h2{text-align:center;color:#555;font-size:18px;font-weight:400;height:35px}.c2{display:block;margin:0 4px;font-size:14px;height:23px;color:#1a0dab;padding-top:10px;text-decoration:none;text-align:center}</style></head><body style=""><div class="bg"><div class="cont"><div class="c1"><img src="https://apkhouse.oss-cn-beijing.aliyuncs.com/vpn/404_02.png" class="img1"></div><h2>哎呀…您访问的页面不存在</h2><div class="c2"><span>%s</span> <img class="img3" src="https://apkhouse.oss-cn-beijing.aliyuncs.com/vpn/404_03.png"></div></div></div></body></html>'

local function isempty(s)
  return s == nil or s == ''
end

redis_module.get_red(
    -- 回调函数 将获取连接池连接，放回连接池操作封装起来
    function (success , red)
		local issbrowsertoken = ngx.var.http_issBrowserToken
		local issbrowserid = ngx.var.http_issBrowserId
		-- 未安装客户端/非合法用户
		if isempty(issbrowserid) then
			ngx.exit(ngx.HTTP_NOT_FOUND)
			return
		elseif isempty(issbrowsertoken) then
			ngx.exit(ngx.HTTP_NOT_FOUND)
			return
		end

		-- redis read value
		local ret_ok = red:get(issbrowserid);
		if ret_ok == ngx.null or ret_ok == nil then
			ngx.header.content_type = 'text/html'
				ngx.say(string.format(template_content, ret_unauth_err))
				ngx.exit(ngx.HTTP_OK)
		else
			if ret_ok ~= issbrowsertoken then
				ngx.header.content_type = 'text/html'
				ngx.say(string.format(template_content, ret_auth_err))
				ngx.exit(ngx.HTTP_OK)
			end
		end
    end
);
