
import random

# Define probabilities
p_sunny = 0.7
p_rainy = 0.3
p_y_given_sunny = 0.2
p_y_given_rainy = 0.8

def importance_sampling1():
    samples = []
    for _ in range(1000):
        # Sample X from according to Baysian Network probabilities
        x_sample = random.choices(['sunny', 'rainy'],weights=[p_sunny, p_rainy])
        x_sample = x_sample[0] 
        # Calculate weight based on evidence Y = yes
        if x_sample == 'sunny':
            weight = p_y_given_sunny 
        else:
            weight = p_y_given_rainy 
        
        samples.append((x_sample, weight))

    total_weight = sum(w for _, w in samples)

    print("Generated Samples:")
    for x, weight in samples:
        print(f"X = {x}, Weight = {weight:.4f}")

    # Calculate posterior probabilities
    posterior_sunny = sum(weight for x, weight in samples if x == 'sunny')/total_weight
    posterior_rainy = sum(weight for x, weight in samples if x == 'rainy')/total_weight

    return posterior_sunny, posterior_rainy

def importance_sampling2():
    samples = []
    for _ in range(1000):
        # Sample X from the proposal distribution (uniform distribution)
        x_sample = random.choice(['sunny', 'rainy'])
        # Calculate weight based on evidence Y = yes
        # In this case you must use p_sunny and p_rainy to correct the weights
        if x_sample == 'sunny':
            weight = p_sunny * p_y_given_sunny 
        else:
            weight = p_rainy * p_y_given_rainy 
        
        samples.append((x_sample, weight))

    total_weight = sum(w for _, w in samples)

    #print("Generated Samples:")
    #for x, weight in samples:
    #    print(f"X = {x}, Weight = {weight:.4f}")

    # Calculate posterior probabilities
    posterior_sunny = sum(weight for x, weight in samples if x == 'sunny')/total_weight
    posterior_rainy = sum(weight for x, weight in samples if x == 'rainy')/total_weight

    return posterior_sunny, posterior_rainy


def calculate_posteriors():
    # Compute marginal probability of evidence Y = yes
    p_y_yes = p_y_given_sunny * p_sunny + p_y_given_rainy * p_rainy

    # Compute posterior probabilities using Bayes' theorem
    posterior_sunny = (p_y_given_sunny * p_sunny) / p_y_yes
    posterior_rainy = (p_y_given_rainy * p_rainy) / p_y_yes
    
    return posterior_sunny, posterior_rainy

def rejection_sampling():
    accepted_samples = []
    for _ in range(5000):  # usually more samples needed due to rejection
        # Sample X from prior
        x_sample = random.choices(['sunny', 'rainy'], weights=[p_sunny, p_rainy])[0]

        # Sample Y from conditional on X
        if x_sample == 'sunny':
            y_sample = random.choices(['yes', 'no'], weights=[p_y_given_sunny, 1 - p_y_given_sunny])[0]
        else:
            y_sample = random.choices(['yes', 'no'], weights=[p_y_given_rainy, 1 - p_y_given_rainy])[0]

        # Accept only if Y == 'yes' (i.e., matches the observed evidence)
        if y_sample == 'yes':
            accepted_samples.append(x_sample)

    # Count accepted samples
    count_sunny = accepted_samples.count('sunny')
    count_rainy = accepted_samples.count('rainy')
    total = count_sunny + count_rainy

    # Compute posteriors
    posterior_sunny = count_sunny / total if total > 0 else 0
    posterior_rainy = count_rainy / total if total > 0 else 0

    return posterior_sunny, posterior_rainy


if __name__ == "__main__":
    posterior_sunny, posterior_rainy = calculate_posteriors()
    print("Posterior Probabilities (Exact Calculations):")
    print(f"P(X = sunny | Y = yes) = {posterior_sunny:.4f}")
    print(f"P(X = rainy | Y = yes) = {posterior_rainy:.4f}")


    posterior_sunny, posterior_rainy = rejection_sampling()
    print("\nPosterior Probabilities (Rejection Sampling):")
    print(f"P(X = sunny | Y = yes) = {posterior_sunny:.4f}")
    print(f"P(X = rainy | Y = yes) = {posterior_rainy:.4f}")


    posterior_sunny, posterior_rainy = importance_sampling1()
    print("\nPosterior Probabilities (Importance Sampling 1):")
    print(f"P(X = sunny | Y = yes) = {posterior_sunny:.4f}")
    print(f"P(X = rainy | Y = yes) = {posterior_rainy:.4f}")

    posterior_sunny, posterior_rainy = importance_sampling2()
    print("\nPosterior Probabilities (Importance Sampling 2):")
    print(f"P(X = sunny | Y = yes) = {posterior_sunny:.4f}")
    print(f"P(X = rainy | Y = yes) = {posterior_rainy:.4f}")

