# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

>   * The profitable path: tokenB->tokenA->tokenD->tokenC->tokenB
>   * amountIn -> amountOut for each swap: (in wei)
    5000000000000000000 tokenB -> 5655321988655321988 tokenA
    5655321988655321988 tokenA -> 2458781317097933552 tokenC
    2458781317097933552 tokenD -> 5088927293301515695 tokenC
    5088927293301515695 tokenC -> 20129888944077446732 tokenB
>   * Final reward (tokenB balance): 20129888944077446732


## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> Slippage in AMM is the "slip" or difference between the expected price and actual price (might happen due to volatility; the drastic ratio change affected by high volume trades or speed of the chain). Uniswap V2 addresses this issue by giving the user ability to specify the slippage tolerance.
>
> Example: Assume the a trader wants to buy 10 tokenA using tokenB, with the liquidity ratio of 1 tokenA : 2000 tokenB, then for some reason the liquidity changes, and the ratio becomes 1 tokenA : 2100 tokenB. Thus, slippage happens, which the trader needs to pay 21000 tokenB instead of expected 20000 tokenB. Uniswap V2 minimizes this risk by allowing the slippage tolerance specification, take swapExactTokensForTokens() function as example.
```solidity
function swapExactTokensForTokens(
    uint256 amountIn,
    uint256 amountOutMin,
    address[] calldata path,
    address to,
    uint256 deadline
) 
...
``` 
> We can specify amountOutMin, which means minimum amountOut acceptable for the user, such that it will revert the transaction should the condition is not satisfied. In above tokenA-tokenB pair case, we can set something like this:
`swapExactTokensForTokens(20000, 9.5, [address(tokenB), address(tokenA)], address(user), block.timestamp+60)`


## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> The minimum liquidity subtraction is designed to lock liquidity in the pool to ensure there is always a minimum liquidity available even if the initial liquidity provider (LP) withdraws its entire share. This design is foundational for the pool, preventing the pool being drained due to immediate withdrawing by LP.  

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> This is to maintain the constant product invariant, to ensure the stability of the pool proportion from the price change of the new liquidity addition or arbitrageurs. 

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

> Sandwich attack is the type of attack on the exchange that exploits time delay between user's transaction submission and execution time on the blockchain. Typically, assuming we are the victim, the attacker will monitor our pending transactions, then front-run our transaction such that the price rises, which will impact to our transaction price being higher, then after that it back-run our transaction causing the price to deplete. Our swap hence could experience slippage and reduce our profit. 

  
    

## Bonus
My Python script [bonus.py](bonus.py) will iteratively search for the , the highest possible amount of tokenB acheived is 27.048947753604427 ether tokenB, with the path: `tokenB->tokenA->tokenD->tokenC->tokenE->tokenD->tokenC->tokenE->tokenD->tokenC->tokenB`. 

However, when I try to execute the path with Arbitrage.t.sol, the operation is reverted. Thus, the highest amount possible to be executed by Arbitrage.t.sol is 22.497221806974142 ether, with path: `tokenB->tokenA->tokenC->tokenE->tokenD->tokenC->tokenB`

