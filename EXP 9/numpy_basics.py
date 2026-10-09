import numpy as np


def main():
    array_1d = np.array([1, 2, 3, 4, 5])
    array_2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    array_3d = np.array(
        [
            [[1, 2, 3], [4, 5, 6]],
            [[7, 8, 9], [10, 11, 12]],
        ]
    )

    print("1D array:\n", array_1d)
    print("2D array:\n", array_2d)
    print("3D array:\n", array_3d)

    other_2d = np.full((3, 3), 2)
    print("\nSecond 2D array:\n", other_2d)
    print("Addition:\n", array_2d + other_2d)
    print("Subtraction:\n", array_2d - other_2d)
    print("Multiplication:\n", array_2d * other_2d)
    print("Division:\n", array_2d / other_2d)

    row_labels = ["A", "B", "C"]
    column_labels = ["X", "Y", "Z"]
    print("\n2D array with character labels:")
    print("  " + "  ".join(column_labels))
    for label, row in zip(row_labels, array_2d):
        print(f"{label} " + "  ".join(str(value) for value in row))


if __name__=="__main__":
    main()
