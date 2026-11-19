import streamlit as st
import sympy as sp

st.set_page_config(
    page_title="Vector Space Analyzer",
    page_icon="📐",
    layout="wide",
)

st.title("Vector Space Basis and Dimension Analyzer")
st.write("Analyze vectors, linear independence, basis and dimension.")

st.subheader("Enter your vectors")
st.write(
    "Enter one vector per line. "
    "Separate the elements using commas."
)

vector_input = st.text_area(
    "Vectors",
    value="1, 2, 3\n2, 4, 6\n1, 1, 0",
    height=150,
)

if st.button("Analyze Vectors"):
    try:
        lines = [line.strip() for line in vector_input.splitlines() if line.strip()]
        if not lines:
            st.error("Enter at least one vector.")
            st.stop()

        vectors = [
            [sp.Rational(value.strip()) for value in line.split(",")]
            for line in lines
        ]

        # Check that all vectors have the same number of elements.
        dimensions = {len(vector) for vector in vectors}
        if len(dimensions) != 1:
            st.error("All vectors must have the same number of elements.")
            st.stop()

        # Create a matrix using the vectors as columns.
        matrix = sp.Matrix(vectors).T

        # Calculate RREF and rank.
        rref_matrix, pivots = matrix.rref()
        rank = matrix.rank()

        # Determine independence and extract a basis for the span.
        independent = rank == len(vectors)
        basis = [vectors[index] for index in pivots]

        st.subheader("1. Original Matrix")
        st.latex(sp.latex(matrix))

        st.subheader("2. Reduced Row Echelon Form")
        st.latex(sp.latex(rref_matrix))

        st.subheader("3. Rank")
        st.write(rank)

        st.subheader("4. Linear Independence")
        if independent:
            st.success("The vectors are linearly independent.")
        else:
            st.warning("The vectors are linearly dependent.")

        st.subheader("5. Basis")
        for index, vector in enumerate(basis, start=1):
            st.write(f"Basis Vector {index}: {vector}")

        st.subheader("6. Dimension")
        st.write(f"Dimension of the span: {rank}")

    except Exception as error:
        st.error(f"Invalid input: {error}")
