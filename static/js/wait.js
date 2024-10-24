function async_try_until_ok__interface_wait(func, ms, args = null) {
    new Promise((resolve, reject) => {
        setTimeout(() => {
            try {
                if (args == null) {
                    func();
                } else {
                    func(args);
                }
                resolve();
            } catch (error) {
                reject();
            }
        }, ms);
    }).then(result => {
        return result;
    }).catch(error => {
        async_try_until_ok__interface_wait(func, ms, args);
    });
}

