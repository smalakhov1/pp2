import matplotlib.pyplot as plt

def plot_2d(X_df, y, ft_x,ft_y):

    x_0 = X_df.loc[y==0, ft_x]
    y_0 = X_df.loc[y==0,ft_y]

    x_1 = X_df.loc[y==1, ft_x]
    y_1 = X_df.loc[y==1,ft_y]

    fig, ax = plt.subplots(figsize=(6,5))

    ax.scatter(
        x_0,
        y_0,
        alpha=0.5,
        label = "No disease"
    )

    ax.scatter(
        x_1,
        y_1,
        alpha=0.5,
        label="Disease"
    )

    ax.set_xlabel(ft_x)
    ax.set_ylabel(ft_y)
    ax.set_title(f"{ft_x} x {ft_y}")
    ax.legend()
    plt.show()

def plot_losses(losses):
    fig, ax = plt.subplots(figsize=(6,4))

    ax.plot(losses)

    ax.set_xlabel("Iteration")
    ax.set_ylabel("Loss")
    ax.set_title("Training loss over iterations")

    plt.show()