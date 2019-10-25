import argparse

from experiment import run


def main(args):
    run(args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # data
    parser.add_argument('--data_root', type=str, default='../inputs/')
    parser.add_argument('--height', type=int, default=672)
    parser.add_argument('--width', type=int, default=512)
    parser.add_argument('--channels', type=int, default=1)
    parser.add_argument('--ts', type=int, default=48)
    parser.add_argument('--input_h', type=int, default=int(672 / 4))
    parser.add_argument('--input_w', type=int, default=int(512 / 4))
    parser.add_argument('--input_ts', type=int, default=24)
    parser.add_argument('--interpolation_mode', type=str, default='nearest')
    parser.add_argument('--n_workers', type=int, default=8)
    # network
    parser.add_argument('--resume', type=str, default=None)
    parser.add_argument('--model', type=str, default='')
    parser.add_argument('--hidden_dims', type=int, nargs='+', default=[16, ])
    parser.add_argument('--n_layers', type=int, default=1)
    # training
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--batch_size', type=int, default=128)
    parser.add_argument('--device', type=str, default='cuda:0')
    parser.add_argument('--loss', type=str, default='L1')
    # optim
    parser.add_argument('--optim_str', type=str, default='Optim/lr=0.001/arg1=1/arg2=2')
    # log
    parser.add_argument('--logdir', type=str, default='../logs')
    parser.add_argument('--freq_to_log_image', type=int, default=1000)
    # misc
    parser.add_argument('--random_seed', type=int, default=42)
    parser.add_argument('--debug', action='store_true', default=False)

    args, _ = parser.parse_known_args()
    main(args)