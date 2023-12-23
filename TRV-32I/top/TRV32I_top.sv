module TRV32I_top #(
    parameter B_WIDTH = 32;
    parameter MEM_SIZE = 32;
) (
    input                   clk, rst;
    output  [31:0]          pc, inst;
    output                  mem_read_en, mem_write_en;
    output  [B_WIDTH-1:0]   mem_data;
);

    wire [B_WIDTH-1:0]      mem_addr;
    wire [(B_WIDTH/8)-1:0]  write_byte_en;


    TRV32I_core TRV32I_core (
        .clk(clk), .rst(rst), .pc(pc), .inst(inst),
        .mem_addr(mem_addr), .mem_data(mem_data),
        .mem_read_en(mem_read_en), .mem_write_en(mem_write_en), .write_byte_en(write_byte_en)
    );


    mem_interface #(
        .B_WIDTH(B_WIDTH)
        .MEM_SIZE(MEM_SIZE)
    ) mem_interface (
        .clk(clk), .rst(rst), .pc(pc), .inst(inst),
        .mem_addr(mem_addr), .mem_data(mem_data),
        .mem_read_en(mem_read_en), .mem_write_en(mem_write_en), .write_byte_en(write_byte_en)
    );


endmodule
