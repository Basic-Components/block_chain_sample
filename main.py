import sys
import argparse
from block_chain_sample.sanic_app import app


def _parser_args(params):
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, help="指定端口")
    args = parser.parse_args(params)
    return args


def main(argv=sys.argv[1:]):
    """执行启动服务的操作."""
    args = _parser_args(argv)
    if args.port:
        app.run(
            host="0.0.0.0", port=args.port
        )
    else:
        app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
