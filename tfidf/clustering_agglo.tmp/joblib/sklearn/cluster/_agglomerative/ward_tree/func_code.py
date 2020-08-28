# first line: 59
    @wraps(f)
    def inner_f(*args, **kwargs):
        extra_args = len(args) - len(all_args)
        if extra_args > 0:
            # ignore first 'self' argument for instance methods
            args_msg = ['{}={}'.format(name, arg)
                        for name, arg in zip(kwonly_args[:extra_args],
                                             args[-extra_args:])]
            warnings.warn("Pass {} as keyword args. From version 0.25 "
                          "passing these as positional arguments will "
                          "result in an error".format(", ".join(args_msg)),
                          FutureWarning)
        kwargs.update({k: arg for k, arg in zip(sig.parameters, args)})
        return f(**kwargs)
