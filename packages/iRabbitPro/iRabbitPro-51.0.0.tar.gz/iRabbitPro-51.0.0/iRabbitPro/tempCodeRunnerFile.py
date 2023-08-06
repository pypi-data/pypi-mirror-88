time.sleep(3)
    api.wx_auth_info()
    print(api.auth_code, api.nickName, api.avatarUrl, api.mobile, api.encryptedData, api.encryptedDataPhone, api.iv, api.ivPhone, api.signature)
    time.sleep(3)
    api.wx_auth_mobile()
    print(api.aut