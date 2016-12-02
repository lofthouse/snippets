#include <math.h>
#include <stdio.h>
#include <string.h>

int a2i(char* string, float* result) {
	char exp=0;
	char has_decimal=0;
	char j=strlen(string)-1;
	unsigned char zero='0';
	unsigned char nine='9';

	while(j>=0) {
		// Valid digit adds by power of place
		if( zero <= string[j] && string[j] <= nine ) {
			*result += ( (string[j]-zero) * pow(10,exp) );
		// Decimal places reset power and divide accumulated result by power of place
		} else if( '.' == string[j] ) {
			// Only one decimal allowed
			if ( has_decimal ) {
				printf("Found a duplicate decimal point at position %d\n", j);
				return 0;
			} else
				has_decimal=1;

			*result /= pow(10,exp);
			exp = -1;
		// Negative signs negate
		} else if( '-' == string[j] ) {
			*result = -*result;
			// Negative signs may only be in the first position
			if( j != 0) {
				printf("Found a negative sign out-of-place  at position %d\n", j);
				return 0;
			} else
				break;
		// and anything else is invalid
		} else {
			printf("Found an invalid character at position %d: %c\n", j, string[j]);
			return 0;
		}

		exp++;
		j--;
	}

	return 1;
}

int main(int argc, char** argv) {
	unsigned char i=1;
	float result;

	while( i < argc ) {
		result=0;

		printf("Argument %d is %s\n", i, argv[i]);
		if( a2i( argv[i], &result ) )
			printf("Its numeric value is %f\n\n", result);
		else
			printf("It is not a valid number\n\n");
		i++;
	}
}
