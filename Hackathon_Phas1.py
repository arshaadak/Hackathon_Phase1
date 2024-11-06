import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Enhanced NAT2 Dataset including the frequencies from the CSV
NAT2_GENOTYPES = {
    'NAT2*4/*4': {
        'acetylator_type': 'Fast',
        'frequency': 3.3,
        'mutations': {
            282: '.',
            341: '.',
            481: '.',
            590: '.',
            803: '.',
            857: '.'
        }
    },
    'NAT2*4/*14': {
        'acetylator_type': 'Intermediate',
        'frequency': 0.8,
        'mutations': {
            282: '.',
            341: '.',
            481: '.',
            590: '.',
            803: 'A',
            857: 'G'
        }
    },
    'NAT2*4/*5': {
        'acetylator_type': 'Intermediate',
        'frequency': 15.0,
        'mutations': {
            282: '.',
            341: 'C',
            481: 'T',
            590: '.',
            803: 'G',
            857: '.'
        }
    },
    'NAT2*5/*5': {
        'acetylator_type': 'Slow',
        'frequency': 24.2,
        'mutations': {
            282: '.',
            341: 'C',
            481: 'T',
            590: '.',
            803: 'G',
            857: '.'
        }
    },
    'NAT2*6/*6': {
        'acetylator_type': 'Slow',
        'frequency': 15.8,
        'mutations': {
            282: 'T',
            341: '.',
            481: '.',
            590: 'A',
            803: '.',
            857: '.'
        }
    }
}


class NAT2Analyzer:
    def __init__(self):
        self.mutation_positions = [282, 341, 481, 590, 803, 857]

    def analyze_genotype(self, mutations):
        for genotype, data in NAT2_GENOTYPES.items():
            if all(mutations.get(pos, '.') == data['mutations'][pos] for pos in self.mutation_positions):
                return (genotype, data['acetylator_type'], data['frequency'])
        return ("Unknown", "Unknown", 0.0)

    def get_dosing_recommendation(self, acetylator_type):
        recommendations = {
            'Fast': {
                'dose': '5-6 mg/kg/day',
                'risk': 'Lower risk of adverse effects, monitor for treatment efficacy',
                'monitoring': 'Regular liver function tests every 3 months',
                'details': 'May require higher doses to maintain therapeutic levels'
            },
            'Intermediate': {
                'dose': '4-5 mg/kg/day',
                'risk': 'Moderate risk of adverse effects',
                'monitoring': 'Liver function tests every 2 months',
                'details': 'Standard dosing usually appropriate'
            },
            'Slow': {
                'dose': '2.5-4 mg/kg/day',
                'risk': 'Higher risk of drug-induced liver injury',
                'monitoring': 'Monthly liver function tests',
                'details': 'Requires reduced dosing to prevent toxicity'
            }
        }
        return recommendations.get(acetylator_type, {
            'dose': 'Consult specialist',
            'risk': 'Unknown',
            'monitoring': 'Frequent monitoring required',
            'details': 'Individual assessment needed'
        })


def create_app():
    st.title("NAT2 Genotype Analysis for Isoniazid Therapy")
    st.write("Personalized dosing recommendations based on NAT2 genetic variations")

    analyzer = NAT2Analyzer()

    tabs = st.tabs(["Patient Analysis", "Population Data", "Information"])

    with tabs[0]:
        st.header("Patient Genotype Analysis")

        cols = st.columns(3)
        mutations = {}

        for i, pos in enumerate(analyzer.mutation_positions):
            with cols[i % 3]:
                mutation = st.selectbox(
                    f"Position {pos}",
                    options=['.', 'A', 'C', 'G', 'T'],
                    key=f"pos_{pos}"
                )
                mutations[pos] = mutation

        if st.button("Generate Recommendations"):
            genotype, acetylator_type, frequency = analyzer.analyze_genotype(mutations)
            recommendations = analyzer.get_dosing_recommendation(acetylator_type)

            col1, col2 = st.columns(2)
            with col1:
                st.success(f"Genotype: {genotype}")
                st.info(f"Acetylator Status: {acetylator_type}")
                st.metric("Population Frequency", f"{frequency}%")

            with col2:
                st.warning(f"Recommended Dose: {recommendations['dose']}")
                st.error(f"Risk Assessment: {recommendations['risk']}")

            st.write("### Clinical Recommendations")
            st.write(recommendations['details'])
            st.write(f"**Monitoring Plan:** {recommendations['monitoring']}")

    with tabs[1]:
        st.header("Population Statistics")

        # Calculate acetylator type frequencies
        frequencies = {
            'Fast': sum(data['frequency'] for data in NAT2_GENOTYPES.values()
                        if data['acetylator_type'] == 'Fast'),
            'Intermediate': sum(data['frequency'] for data in NAT2_GENOTYPES.values()
                                if data['acetylator_type'] == 'Intermediate'),
            'Slow': sum(data['frequency'] for data in NAT2_GENOTYPES.values()
                        if data['acetylator_type'] == 'Slow')
        }

        # Plotly Bar Chart for Acetylator Frequencies
        acetylator_df = pd.DataFrame(list(frequencies.items()), columns=["Acetylator Type", "Frequency"])
        fig_bar = px.bar(acetylator_df, x="Acetylator Type", y="Frequency", title="Acetylator Type Distribution",
                         color="Acetylator Type", text="Frequency")
        fig_bar.update_layout(yaxis_title="Frequency (%)")
        st.plotly_chart(fig_bar, use_container_width=True)

        # Detailed genotype distribution Pie Chart
        genotype_df = pd.DataFrame([
            {
                'Genotype': genotype,
                'Acetylator Type': data['acetylator_type'],
                'Frequency': data['frequency']
            }
            for genotype, data in NAT2_GENOTYPES.items()
        ])

        fig_pie = px.pie(genotype_df, values='Frequency', names='Genotype', title="Genotype Frequency Distribution",
                         hover_data=['Acetylator Type'], hole=0.3)
        st.plotly_chart(fig_pie, use_container_width=True)

    with tabs[2]:
        st.header("About NAT2 Testing")
        st.write("""
        ### Clinical Significance
        NAT2 genetic testing helps identify a patient's acetylator status, which 
        influences isoniazid metabolism in tuberculosis treatment. This information 
        is crucial for:
        - Optimizing drug dosage
        - Minimizing adverse effects
        - Improving treatment outcomes

        ### Interpretation Guide
        - Fast acetylators: Higher doses may be needed
        - Intermediate acetylators: Standard dosing usually appropriate
        - Slow acetylators: Lower doses recommended to prevent toxicity

        ### Important Notes
        - This tool is for research and educational purposes
        - Clinical decisions require healthcare professional judgment
        - Regular monitoring is essential for all patients
        """)


if __name__ == "__main__":
    create_app()
