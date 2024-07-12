from functools import wraps
import click


def mutually_exclusive_options(*option_pairs):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            for train_opt, pretrained_opt in option_pairs:
                train_value = kwargs.get(train_opt)
                pretrained_value = kwargs.get(pretrained_opt)

                if train_value and pretrained_value:
                    raise click.UsageError(
                        f"Options --{train_opt} and --{pretrained_opt} are mutually exclusive."
                    )

                if not train_value and not pretrained_value:
                    raise click.UsageError(
                        f"At least one of --{train_opt} or --{pretrained_opt} must be specified."
                    )

            return f(*args, **kwargs)

        return wrapper

    return decorator
